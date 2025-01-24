<h1> File Summary API</h1>


A FastAPI-based application for uploading, processing, and summarizing document files. This API supports extracting content from uploaded files, generating summaries using OpenAI, and storing file metadata in a PostgreSQL or SQLite database.

Features
--------

*   **File Upload and Processing:**
Accepts .pdf, .docx, and .txt files.
Extracts content using textract.
Summarizes content using OpenAI (e.g., GPT models).

*   **Database Management:**
Stores metadata for each file (name, path, format, size, summary).
Supports PostgreSQL for production and SQLite for testing.

*   **RESTful Endpoints:**
Upload and process files in parallel.
List all uploaded files.
Retrieve file content or summaries by ID.



