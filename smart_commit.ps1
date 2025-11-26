# Smart Commit Script
# Automatically pulls before committing tracker files

param(
    [string]$Message = "Update tracker data"
)

$ErrorActionPreference = "Stop"

Write-Host "[INFO] Checking for tracker file changes..." -ForegroundColor Cyan

# Check if tracker files are modified
$trackerFiles = git status --porcelain | Select-String -Pattern '(cold_emails\.json|job_applications\.json)'

if ($trackerFiles) {
    Write-Host "[PULL] Tracker files modified. Pulling latest changes first..." -ForegroundColor Yellow
    
    # Pull latest
    git pull --rebase origin main
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Pull failed. Please resolve conflicts manually." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[SUCCESS] Synced with remote." -ForegroundColor Green
}

# Stage all changes
git add .

# Commit
Write-Host "[COMMIT] Committing changes..." -ForegroundColor Cyan
git commit -m $Message

# Push
Write-Host "[PUSH] Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

Write-Host "[SUCCESS] All done!" -ForegroundColor Green
