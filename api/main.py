import asyncio
import os
import shutil
from typing import Annotated, List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from api.db_config import Base, engine, get_db
from api.models import (
    FileContentResponse,
    FileListResponse,
    FileMetadata,
    FileSummaryResponse,
)
from api.settings import settings
from api.utils import extract_file_content, get_summary_from_openai

UPLOAD_FOLDER = "./uploaded_files"

# Make sure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create all db tables on start up
Base.metadata.create_all(bind=engine)

SessionDep = Annotated[Session, Depends(get_db)]

# General API setup
app = FastAPI(
    title="File Summary API",
    description="API for file processing",
    version=settings.VERSION,
    swagger_ui_parameters={"tryItOutEnabled": True},
)


async def process_file(uploaded_file: UploadFile, db: Session) -> dict:
    """
    Asynchronously processes a single file: saves it, extracts content, generates a summary,
    and stores metadata in the database.
    """
    file_name = uploaded_file.filename
    file_format = os.path.splitext(file_name)[-1].lower()

    if file_format not in [".pdf", ".docx", ".doc", ".txt"]:
        return {"name": file_name, "status": "skipped", "reason": "Unsupported format."}

    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    existing_file = db.query(FileMetadata).filter(FileMetadata.path == file_path).first()
    if existing_file:
        return {"name": file_name, "status": "skipped", "reason": "File already exists."}

    try:
        # Save the file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file.file, f)

        # Extract file content
        content = extract_file_content(file_path)

        # Generate summary asynchronously
        summary = await get_summary_from_openai(content)

        # Get file size
        file_size = os.path.getsize(file_path)

        # Store file metadata in the database
        file_metadata = FileMetadata(
            name=file_name,
            path=file_path,
            format=file_format.lstrip("."),
            size=file_size,
            summary=summary,
        )
        db.add(file_metadata)
        db.commit()

        return {
            "name": file_name,
            "status": "processed",
            "path": file_path,
            "format": file_format.lstrip("."),
            "size": file_size,
            "summary": summary,
        }

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
        return {"name": file_name, "status": "error", "reason": str(e)}


@app.post("/refresh")
async def refresh_files(
    files: list[UploadFile] = File(...),  # Accept multiple file uploads
    db: Session = Depends(get_db),
):
    """
    Processes uploaded document files in parallel, extracts their content,
    generates summaries using ChatGPT, and stores metadata in the database.
    """
    tasks = [process_file(file, db) for file in files]
    # Process all files in parallel in separate tasks
    results = await asyncio.gather(*tasks)

    processed_files = [result for result in results if result["status"] == "processed"]
    skipped_files = [result for result in results if result["status"] == "skipped"]
    errored_files = [result for result in results if result["status"] == "error"]

    if not processed_files:
        raise HTTPException(
            status_code=404,
            detail="No valid or new files were processed.",
        )

    return {
        "message": "Files processed successfully.",
        "processed_files": processed_files,
        "skipped_files": skipped_files,
        "errored_files": errored_files,
    }


@app.get("/files", response_model=List[FileListResponse])
def list_files(db: SessionDep):
    """Lists all files in the db."""
    files = db.query(FileMetadata).all()
    return files


@app.get("/files/{id}/summary", response_model=FileSummaryResponse)
def get_file_summary(id: int, db: SessionDep):
    """Retrieves the summary of the file by ID."""
    file = db.query(FileMetadata).filter(FileMetadata.id == id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
    return {"id": file.id, "summary": file.summary}


@app.get("/files/{id}/content", response_model=FileContentResponse)
def get_file_content(id: int, db: Session = Depends(get_db)):
    """
    Retrieves the content of a file by the ID from the database.
    """
    # Query the database for the file
    file_metadata = db.query(FileMetadata).filter(FileMetadata.id == id).first()

    # File with this id might not exist in the db or it's not uploaded correctly.
    if not file_metadata or not os.path.exists(file_metadata.path):
        raise HTTPException(
            status_code=404,
            detail=f"File with ID {id} not found or it's content can't be extracted.",
        )

    try:
        # Extract file content
        content = extract_file_content(file_metadata.path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract file content: {str(e)}")

    # Return the file content
    return FileContentResponse(id=file_metadata.id, content=content)
