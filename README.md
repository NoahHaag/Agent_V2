# AI Agent V2

This project implements an advanced AI Agent capable of performing various tasks including:
- **Gmail Integration**: Reading, searching, and drafting emails.
- **Document Analysis**: Reading and analyzing PDF and Word documents.
- **Job Application Tracking**: Managing job applications with a built-in tracker.
- **Cover Letter Generation**: Automatically generating personalized cover letters based on your CV and job descriptions.
- **Research**: Searching and retrieving information from a local database of research papers.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Agent_V2
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY="your_google_api_key"
    GOOGLE_ENVIRON_SECRET="your_google_environ_secret"
    ```

4.  **Google Credentials:**
    - Place your `credentials.json` (OAuth 2.0 Client IDs) in the root directory.
    - The first time you run the agent, it will authenticate and generate `token.json`.

## Usage

Run the agent using:
```bash
python agent.py
```

## Features

-   **Gmail Tools**: `search_gmail`, `get_gmail_message`, `create_gmail_draft`
-   **Document Tools**: `read_document` (PDF/Docx), `search_pdf` (ChromaDB)
-   **Job Tracker**: `add_job_application`, `update_job_application`, `get_job_applications`
-   **Cover Letter**: `generate_cover_letter`

## Structure

-   `agent.py`: Main entry point and agent logic.
-   `tools_2.py`: Implementation of various tools (Gmail, Job Tracker, etc.).
-   `documents/`: Folder to store your CV and other documents.
-   `cover_letters/`: Generated cover letters are saved here.
-   `job_applications.json`: Database for tracked job applications.
