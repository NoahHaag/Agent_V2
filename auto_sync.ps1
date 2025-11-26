# Auto-Sync Script for Job Assistant
# This script automatically commits and pushes tracker data to GitHub

$ErrorActionPreference = "Stop"
$RepoPath = "d:\Python Projects\AI Agents\Agent_V2"

try {
    # Navigate to repository
    Set-Location $RepoPath
    Write-Host "[INFO] Working directory: $RepoPath" -ForegroundColor Cyan
    
    # Add tracker files
    git add cold_emails.json job_applications.json
    
    # Check if there are changes to commit
    git diff --staged --quiet
    
    if ($LASTEXITCODE -ne 0) {
        # There are changes - commit and push
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "Auto-sync: Update tracker data [$timestamp]"
        git push origin main
        
        Write-Host "[SUCCESS] Synced to GitHub at $timestamp" -ForegroundColor Green
    }
    else {
        # No changes
        Write-Host "[INFO] No changes to sync" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[ERROR] Sync failed: $_" -ForegroundColor Red
    exit 1
}
