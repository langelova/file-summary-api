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



### Prerequisites

Ensure you have the following installed on your machine:

*   Docker

*   Docker Compose


### Installation

1.  **Clone the Repository**:

```
git clone https://github.com/langelova/file-summary-api.git
```

2.  **Create a .env file following example.env**:

```
NOTE: You'll need a working API key for OpenAI
```

3.  **Build and start containers**:

```
docker-compose up --build
```

4. **Run tests**:
```
docker compose run --rm app sh -c "pytest"
```

5. **Interact with the api**:
```
http://localhost:5000/docs/
```

