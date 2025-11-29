# AI Agent V2

This project implements an advanced AI Agent capable of performing various tasks including:

- **Gmail Integration**: Reading, searching, and drafting emails.
- **Document Analysis**: Reading and analyzing PDF and Word documents.
- **Job Application Tracking**: Managing job applications with a built-in tracker.
- **Cover Letter Generation**: Automatically generating personalized cover letters based on your CV and job descriptions.
- **Job Search Automation** 🆕: Automated job discovery using SerpAPI (aggregates LinkedIn, Indeed, Glassdoor)
- **Cold Email Tracking**: Track outreach to professors and researchers with network visualization
- **Research**: Searching and retrieving information from a local database of research papers.

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd Agent_V2
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:

    ```env
    GOOGLE_API_KEY="your_google_api_key"
    GOOGLE_ENVIRON_SECRET="your_google_environ_secret"
    SERPAPI_KEY="your_serpapi_key"  # For job search (100 free searches/month)
    ```

4. **Google Credentials:**
    - Place your `credentials.json` (OAuth 2.0 Client IDs) in the root directory.
    - The first time you run the agent, it will authenticate and generate `token.json`.

5. **SerpAPI Setup (Optional - for job search):**
    - Sign up for free at [serpapi.com](https://serpapi.com/) (no credit card required)
    - Get your API key and add to `.env`
    - See `JOB_SEARCH_SETUP.md` for detailed instructions

## Usage

Run the agent using:

```bash
python agent.py
```

## Features

- **Gmail Tools**: `search_gmail`, `get_gmail_message`, `create_gmail_draft`
- **Document Tools**: `read_document` (PDF/Docx), `search_pdf` (ChromaDB)
- **Job Tracker**: `add_job_application`, `update_job_application`, `get_job_applications`
- **Cover Letter**: `generate_cover_letter`
- **Job Search** 🆕:
  - `search_jobs` - Search LinkedIn, Indeed, Glassdoor, etc. (via SerpAPI)
  - `get_job_opportunities` - View saved opportunities
  - `get_serpapi_usage_report` - Check API usage
  - **Automated monitoring** via GitHub Actions (weekdays @ 9 AM)
- **Cold Email Tracker**: Track outreach with `add_cold_email`, `update_cold_email`, `query_cold_emails`
- **Network Graph**: Visualize professional connections with `generate_network_graph`

## Structure

- `agent.py`: Main entry point and agent logic.
- `tools_2.py`: Implementation of various tools (Gmail, Job Tracker, Job Search, etc.).
- `documents/`: Folder to store your CV and other documents.
- `cover_letters/`: Generated cover letters are saved here.
- `job_applications.json`: Database for tracked job applications.
- `job_opportunities.json`: Discovered job opportunities (not yet applied).
- `cold_emails.json`: Track cold emails to researchers/professors.
- `serpapi_usage.json`: API usage tracking (stays under 100/month limit).
- `.github/workflows/job_monitor.yml`: Automated job search workflow.

## Automated Job Monitoring

The GitHub Action automatically searches for jobs Monday-Friday:

- Uses ~40 searches/month (leaves 60 for manual use)
- Commits new opportunities to the repo
- Stops automatically if approaching limit
- See `JOB_SEARCH_SETUP.md` for setup instructions
