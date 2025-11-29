# 🤖 AI Career Assistant - Advanced Multi-Tool Agent

> **An intelligent AI agent built with Google ADK for automating job search, email management, application tracking, and professional networking.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4)](https://github.com/google/adk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

This project showcases a **production-ready AI agent** that integrates multiple APIs and services to automate the entire job search workflow. Built with Google's Agent Development Kit (ADK), it demonstrates advanced capabilities including:

- 🔍 **Automated Job Discovery** - Multi-source job aggregation via SerpAPI (LinkedIn + Indeed + Glassdoor + ZipRecruiter)
- 📧 **Gmail Integration** - Full email management with OAuth 2.0 authentication
- 📊 **Intelligent Tracking** - Job applications, cold emails, and professional network visualization
- 🤖 **Smart Automation** - GitHub Actions workflows for scheduled job searches
- 📝 **AI-Powered Content Generation** - Cover letters tailored to job descriptions
- 🧠 **Persistent Memory** - SQLite-backed session management with automatic summarization

---

## ✨ Key Features

### 🔎 Job Search Automation

- **Multi-platform aggregation**: Searches 10+ job sites simultaneously (LinkedIn, Indeed, Glassdoor, ZipRecruiter, Monster, CareerBuilder)
- **Smart deduplication**: Prevents saving duplicate job postings
- **Usage tracking**: Built-in quota management for API limits (200 searches/month)
- **GitHub Actions integration**: Automated daily searches with configurable queries
- **Natural language interface**: "Search for marine scientist jobs in Florida posted this week"

### 📧 Email & Communication

- **Gmail API integration**: Read, search, and draft emails
- **Cold email tracking**: Track outreach to researchers/professors with status updates
- **Network visualization**: Mermaid.js graphs showing professional connections and referrals
- **Email summarization**: AI-powered summaries of email threads
- **Draft generation**: Create professional outreach emails based on context

### 📋 Application Management

- **Full application lifecycle**: Track from discovery → application → interview → offer
- **Cover letter automation**: AI-generated, personalized cover letters (Word + PDF)
- **Document parsing**: Extract data from job descriptions and CVs
- **Status tracking**: Monitor deadlines, follow-ups, and next actions
- **Integration**: Seamless flow from discovering jobs to applying

### 🧠 Intelligence & Memory

- **Vector search**: ChromaDB integration for research paper retrieval
- **Session persistence**: SQLite database with conversational memory
- **Automatic summarization**: Compresses long conversations to prevent degradation
- **Tool orchestration**: Dynamic sub-agent delegation for specialized tasks
- **Error recovery**: Graceful handling of API failures and rate limits

### 🤖 Automation & DevOps

- **GitHub Actions workflows**: Scheduled job searches (Monday-Friday @ 9 AM EST)
- **Automated commits**: Results pushed to repository with structured messages
- **Environment management**: Secure credential handling via GitHub Secrets
- **Multi-environment support**: Local development + cloud execution
- **Monitoring**: Usage reports and API quota tracking

---

## 🏗️ Architecture

### Agent Structure

```
Root Agent (Gemini 2.5 Flash)
├── Gmail Search Agent (specialized sub-agent)
├── Google Search Agent (specialized sub-agent)
└── Tools Ecosystem:
    ├── Gmail Tools (read, draft, search)
    ├── Job Search (SerpAPI integration)
    ├── Document Tools (PDF/DOCX parsing)
    ├── Job Tracker (CRUD operations)
    ├── Cover Letter Generator (LLM + formatting)
    ├── Cold Email Tracker (network analysis)
    ├── Memory Tools (load/preload/summarize)
    └── Research Tools (ChromaDB vector search)
```

### Technology Stack

- **Agent Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash / Flash Lite
- **APIs**: Gmail API, SerpAPI, Google Search
- **Storage**: SQLite (sessions), JSON (structured data)
- **Vector DB**: ChromaDB with embedding functions
- **Document Processing**: PyPDF2, python-docx, ReportLab
- **Automation**: GitHub Actions, Python asyncio
- **Authentication**: OAuth 2.0 (Google), Environment variables

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Project (for Gmail API)
- SerpAPI account (free tier: 200 searches/month)

### Installation

1. **Clone & Install**

   ```bash
   git clone <repository-url>
   cd Agent_V2
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   # Create .env file
   cat > .env << EOF
   GOOGLE_API_KEY="your_gemini_api_key"
   SERPAPI_KEY="your_serpapi_key"
   EOF
   ```

3. **Setup Gmail API**
   - Download `credentials.json` from Google Cloud Console
   - Place in project root
   - Run agent (will authenticate and create `token.json`)

4. **Run Agent**

   ```bash
   python agent.py
   ```

### Example Usage

```
You: Search for marine scientist jobs in Florida posted this week
Agent: ✅ Found 12 jobs, 8 new opportunities saved!

You: Show me the opportunities
Agent: 📋 Found 8 job opportunities:
       1. Marine Scientist - NOAA
          📍 Key West, FL | Via: LinkedIn | $65K-$80K
          🔗 https://...

You: I want to apply to job ID abc123
Agent: ✅ Added to job tracker. Generate cover letter?

You: Yes, generate a cover letter
Agent: ✅ Cover letter generated!
       📄 cover_letters/NOAA_Marine_Scientist_2025-11-29.docx
```

---

## 🛠️ Available Tools & Commands

### Job Search

```python
search_jobs(query, location, date_posted)        # Search for jobs
get_job_opportunities(days_back, company, title) # View saved jobs
get_serpapi_usage_report()                       # Check API usage
```

### Application Tracking

```python
add_job_application(company, position, ...)      # Track new application
update_job_application(company, status, ...)     # Update status
get_job_applications(status, company, ...)       # Query applications
generate_cover_letter(company, position, ...)    # AI cover letter
```

### Email & Networking

```python
add_cold_email(recipient_name, email, ...)       # Track outreach
update_cold_email(recipient_name, status, ...)   # Update status
query_cold_emails(status, institution, ...)      # Query emails
generate_network_graph()                         # Visualize network
```

### Document & Research

```python
read_document(filename)                          # Parse CV/resume
search_pdf(query)                                # Vector search papers
```

---

## 📊 Automated Job Monitoring

### GitHub Actions Workflow

The agent runs **automated job searches** via GitHub Actions:

- **Schedule**: Monday-Friday @ 9 AM EST
- **Searches**: 3 configurable queries (customizable in `run_job_search.py`)
- **Results**: Committed to repository with timestamp
- **Quota Management**: Stops at 190/200 searches (safety margin)

**Setup**:

1. Add `SERPAPI_KEY` to GitHub Secrets
2. Configure search queries in `run_job_search.py`
3. Push to GitHub - workflow runs automatically

**Monthly Budget**:

- Automated: ~60 searches (3 queries × ~20 weekdays)
- Manual: 140 remaining for interactive use
- Total: 200 searches/month (free tier)

---

## 📁 Project Structure

```
Agent_V2/
├── agent.py                          # Main entry point
├── tools_2.py                        # Tool implementations (1400+ lines)
├── run_job_search.py                 # Standalone script for automation
├── .github/workflows/
│   └── job_monitor.yml               # GitHub Actions workflow
├── documents/                        # CV storage
├── cover_letters/                    # Generated cover letters
├── job_applications.json             # Application tracker
├── job_opportunities.json            # Discovered jobs
├── cold_emails.json                  # Outreach tracker
├── serpapi_usage.json                # API quota tracking
├── my_agent_data.db                  # SQLite session storage
└── JOB_SEARCH_SETUP.md              # Detailed setup guide
```

---

## 🎓 Technical Highlights

### Advanced Agent Design

- **Multi-agent architecture**: Specialized sub-agents for search tasks
- **Tool orchestration**: Dynamic tool selection based on user intent
- **Error handling**: Graceful degradation with informative messages
- **Async operations**: Non-blocking API calls and database operations

### Data Management

- **Deduplication**: Smart matching on company + title + location
- **Vector search**: Semantic retrieval from research papers
- **Session persistence**: Conversational context across restarts
- **Memory compression**: Automatic summarization after 40 events

### API Integration

- **OAuth 2.0**: Secure Gmail authentication
- **Rate limiting**: Built-in quota tracking for SerpAPI
- **Error recovery**: Retry logic with exponential backoff
- **Multi-source**: Aggregates data from 10+ job platforms

### Automation

- **Cron scheduling**: GitHub Actions for recurring searches
- **Version control**: Results tracked in git for history
- **Environment awareness**: Adapts to local vs. GitHub Actions
- **Monitoring**: Usage reports and warnings

---

## 📈 Usage Statistics

- **Lines of Code**: ~2,000+ (excluding dependencies)
- **Tools Implemented**: 20+ functional tools
- **APIs Integrated**: 4 (Gmail, SerpAPI, Google Search, ChromaDB)
- **Data Formats**: JSON, SQLite, PDF, DOCX, Markdown
- **Automation**: GitHub Actions, async task scheduling

---

## 🔒 Security

- Environment variables for API keys
- OAuth 2.0 for Gmail access
- GitHub Secrets for CI/CD
- No hardcoded credentials
- Token refresh handling

---

## 📚 Documentation

- `JOB_SEARCH_SETUP.md` - Comprehensive setup guide for job search automation
- `README.md` - This file
- Inline documentation in all Python modules
- Detailed docstrings for all functions

---

## 🤝 Contributing

This is a personal project demonstrating AI agent capabilities. Feel free to fork and adapt for your own use case.

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Google ADK for the agent framework
- SerpAPI for job aggregation
- LangChain community for Gmail integration

---

## 📞 Contact

**Noah Haag** - Marine Biologist & AI Engineer

- GitHub: [https://github.com/NoahHaag]
- LinkedIn: [https://www.linkedin.com/in/noah-haag-961691161/]
- Email: [noahhaag1998@gmail.com]

---

**Built with Google ADK | Powered by Gemini 2.5 Flash**
