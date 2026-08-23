# TravelAI Backend Startup Script

Write-Host "--- TravelAI Backend Diagnostic ---" -ForegroundColor Cyan

# 1. Check MongoDB
Write-Host "[1/3] Checking MongoDB..." -NoNewline
$mongoProcess = Get-NetTCPConnection -LocalPort 27017 -ErrorAction SilentlyContinue
if ($mongoProcess) {
    Write-Host " RUNNING" -ForegroundColor Green
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Warning "MongoDB does not appear to be running on port 27017. Please start MongoDB Service."
}

# 2. Check Virtual Environment
Write-Host "[2/3] Checking Python Environment..." -NoNewline
if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host " FOUND" -ForegroundColor Green
} else {
    Write-Host " MISSING" -ForegroundColor Red
    Write-Warning "Virtual environment not found. Run 'python -m venv .venv' and install requirements."
    exit
}

# 3. Start Server
Write-Host "[3/3] Starting Uvicorn Server on http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "Note: Emulator uses http://10.0.2.2:8000 to reach this host." -ForegroundColor Gray

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
