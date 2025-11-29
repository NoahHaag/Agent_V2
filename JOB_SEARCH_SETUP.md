# 🔍 Job Search Tool - Setup Guide

## Overview

Your agent now has automated job search capabilities using SerpAPI! This tool:

- ✅ Searches **LinkedIn, Indeed, Glassdoor, ZipRecruiter** and more (all in one)
- ✅ **100 free searches/month** (no credit card required)
- ✅ **Automatic usage tracking** (never exceed your limit)
- ✅ **Deduplication** (won't save the same job twice)
- ✅ **GitHub Actions integration** (automated daily searches)

---

## 🚀 Quick Start (5 minutes)

### Step 1: Get SerpAPI Key

1. Go to [serpapi.com](https://serpapi.com/)
2. Sign up for a free account (no credit card required)
3. Go to "My Account" → "API Key"
4. Copy your API key

### Step 2: Add to Local Environment

Add to your `.env` file:

```env
SERPAPI_KEY="your_api_key_here"
```

### Step 3: Test Locally

Run your agent and try:

```
You: Search for marine scientist jobs in Florida
You: Show me the job opportunities you found
You: How many SerpAPI searches do I have left this month?
```

---

## 🤖 GitHub Actions Setup (Automated Searches)

### Step 1: Add Secret to GitHub

1. Go to your repo: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `SERPAPI_KEY`
4. Value: Your SerpAPI key
5. Click **Add secret**

### Step 2: Configure Search Queries

Edit `run_job_search.py` (lines 13-25):

```python
JOB_SEARCHES = [
    {
        "query": "Marine Scientist",      # Your job title
        "location": "Florida, USA",       # Your location
        "date_posted": "week"             # today, 3days, week, month
    },
    {
        "query": "Research Biologist",
        "location": "Remote",
        "date_posted": "week"
    }
]
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add job search automation"
git push
```

### Step 4: Verify Workflow

1. Go to **Actions** tab in your repo
2. You should see "Job Monitor" workflow
3. Click **Run workflow** to test manually
4. It will run automatically **Monday-Friday at 9 AM EST**

---

## 📊 Usage Management

### Check Usage Anytime

```
You: How many SerpAPI searches have I used this month?
```

### Current Setup (Stay Under 100/month)

- **Automated searches**: ~40/month (2 searches × weekdays only)
- **Manual searches**: 60 remaining for you
- **Auto-stops at**: 95 searches (leaves 5 as buffer)
- **Resets**: 1st of each month

### Adjust Limits

If you want to change the safety limit, edit `tools_2.py`:

```python
def search_jobs(..., usage_limit: int = 95, ...):  # Change 95 to your limit
```

---

## 🎯 How to Use

### Search for Jobs

```
You: Search for marine biologist positions in Boston
You: Find research scientist jobs posted this week
You: Look for remote data science jobs
```

### View Opportunities

```
You: Show me all saved job opportunities
You: Show jobs from the last 7 days
You: Show me NOAA jobs
You: Filter jobs with "Marine" in the title
```

### Apply Workflow

```
You: Show me opportunities
You: I want to apply to job ID abc12345
[Agent will add to job tracker, optionally generate cover letter]
```

### Delete Jobs

```
You: Delete job opportunity abc12345
```

---

## 📁 Data Files

- **`job_opportunities.json`**: All discovered jobs (tracked in git)
- **`serpapi_usage.json`**: API usage history (tracked in git)
- **`job_applications.json`**: Jobs you've applied to (existing)

---

## 🔄 Automated Workflow

The GitHub Action runs automatically:

1. **When**: Weekdays at 9 AM EST
2. **What it does**:
   - Runs your predefined searches
   - Saves new jobs to `job_opportunities.json`
   - Commits changes to repo
   - Stops if usage limit reached
3. **How to see results**:
   - Check your repo for new commits (🔍 Auto: New job opportunities...)
   - Pull latest changes: `git pull`
   - Ask agent: "Show me opportunities from today"

---

## 💡 Pro Tips

1. **Review opportunities weekly**: `Show me jobs from the last 7 days`
2. **Track usage regularly**: Check usage before month-end
3. **Customize searches**: Edit `run_job_search.py` for your target roles
4. **Integrate with applications**: When you apply, move from opportunities → job tracker
5. **Morning routine**: Pull repo, review new jobs, apply to best matches

---

## 🐛 Troubleshooting

### "SERPAPI_KEY not found"

- Make sure it's in `.env` file locally
- Make sure it's added to GitHub Secrets for Actions

### "Usage limit reached"

- Check: `You: How many searches have I used?`
- Wait until next month (resets on 1st)
- Or adjust `usage_limit` parameter

### GitHub Action not running

- Check **Actions** tab → **Job Monitor** → View logs
- Verify `SERPAPI_KEY` is in GitHub Secrets
- Check workflow file syntax

### No new jobs found

- Searches might be returning duplicates (working as intended)
- Try different search queries
- Check date filter (maybe broaden from "today" to "week")

---

## ✅ You're All Set

Your job search is now automated!

**Next steps:**

1. Test locally: `You: Search for jobs`
2. Add `SERPAPI_KEY` to GitHub Secrets
3. Push to trigger automated monitoring
4. Check back daily for new opportunities

Questions? Ask your agent: `How do I use the job search tool?`
