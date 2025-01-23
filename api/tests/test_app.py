import os
import tempfile

from api.utils import extract_file_content


def test_get_files_endpoint(client):
    """
    Test the /files endpoint to list files.
    """
    response = client.get("/files")
    assert response.status_code == 200
    files = response.json()
    assert len(files) == 3
    assert files[0]["name"] == "file1.txt"
    assert files[0]["format"] == "txt"


def test_get_file_summary_endpoint(client):
    """
    Test the /files/{id}/summary endpoint.
    """
    # # Upload a file first
    # file_content = "This is a test file content."
    # files = [("files", ("test.txt", file_content, "text/plain"))]
    # client.post("/refresh", files=files)

    # Fetch the summary
    response = client.get("/files/1/summary")
    assert response.status_code == 200
    assert response.json()["summary"] is not None


def test_refresh_endpoint(client):
    """
    Test the /refresh endpoint to upload files.
    """
    # Simulate uploading a file
    file_content = "This is a test file content."
    files = [("files", ("test.txt", file_content, "text/plain"))]

    response = client.post("/refresh", files=files)

    assert response.status_code == 200
    assert "Files processed successfully." in response.json()["message"]
    processed_files = response.json()["processed_files"]
    assert len(processed_files) == 1
    assert processed_files[0]["name"] == "test.txt"


def test_extract_file_content():
    """Test text extraction from a file."""
    # Create a temporary file with some text
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Hello, this is a test file.")
        temp_file_path = temp_file.name

    # Test the extraction
    content = extract_file_content(temp_file_path)
    assert content == "Hello, this is a test file."

    # Cleanup
    os.remove(temp_file_path)
