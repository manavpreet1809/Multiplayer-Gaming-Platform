# Start MongoDB (if needed), FastAPI, and the React dev server (Windows / PowerShell).
# Usage: from repo root: .\scripts\dev-windows.ps1
# If execution policy blocks scripts: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

function Test-PortListening {
    param([int]$Port)
    $c = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return $null -ne $c
}

$mongoProc = $null
$uvicornProc = $null

function Stop-DevProcesses {
    if ($null -ne $uvicornProc -and -not $uvicornProc.HasExited) {
        Stop-Process -Id $uvicornProc.Id -Force -ErrorAction SilentlyContinue
    }
    if ($null -ne $mongoProc -and -not $mongoProc.HasExited) {
        Stop-Process -Id $mongoProc.Id -Force -ErrorAction SilentlyContinue
    }
}

try {
    if ($env:SKIP_MONGO -eq "1") {
        Write-Host "SKIP_MONGO=1: not starting mongod (using existing MongoDB)."
    }
    elseif (Test-PortListening -Port 27017) {
        Write-Host "Port 27017 already in use — assuming MongoDB is running."
    }
    else {
        $dataPath = if ($env:MONGO_DATA) { $env:MONGO_DATA } else { Join-Path $env:USERPROFILE "mongodb-data" }
        New-Item -ItemType Directory -Force -Path $dataPath | Out-Null
        $mongodExe = Get-Command mongod -ErrorAction SilentlyContinue
        if (-not $mongodExe) {
            Write-Error "mongod not found in PATH. Install MongoDB Community Server or set SKIP_MONGO=1."
        }
        Write-Host "Starting MongoDB (dbpath $dataPath)..."
        $mongoProc = Start-Process -FilePath $mongodExe.Source `
            -ArgumentList "--dbpath", $dataPath `
            -PassThru -WindowStyle Hidden
        Start-Sleep -Seconds 2
    }

    $venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Error "Missing .venv. Run: py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt"
    }

    $env:PYTHONPATH = "src"
    Write-Host "Starting FastAPI (uvicorn)..."
    $uvicornProc = Start-Process -FilePath $venvPython `
        -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000" `
        -WorkingDirectory $RepoRoot `
        -PassThru -WindowStyle Hidden

    Start-Sleep -Seconds 1

    $frontend = Join-Path $RepoRoot "frontend"
    if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
        Write-Host "Installing frontend dependencies (first run)..."
        Set-Location $frontend
        npm install
    }
    else {
        Set-Location $frontend
    }

    Write-Host "Starting React (npm start). Press Ctrl+C to stop."
    npm start
}
finally {
    Stop-DevProcesses
}
