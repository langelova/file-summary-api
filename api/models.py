from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String

from .db_config import Base


class FileMetadata(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, unique=True, index=True)
    format = Column(String)
    size = Column(Float)
    summary = Column(String, nullable=True)


# Pydantic Models
class FileListResponse(BaseModel):
    id: int
    name: str
    format: str
    path: str

    class Config:
        from_attributes = True


class FileSummaryResponse(BaseModel):
    id: int
    summary: str

    class Config:
        from_attributes = True


class FileContentResponse(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True
