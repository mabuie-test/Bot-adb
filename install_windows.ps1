# install_windows.ps1
# Run from project root using PowerShell (administrator not strictly required for venv)
# Usage: .\install_windows.ps1

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python not found in PATH. Install Python 3.10+ from https://www.python.org/downloads/ and re-run."
    exit 1
}

# create venv
python -m venv venv
& .\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install requirements
python -m pip install -r requirements.txt

Write-Host "Virtualenv created and requirements installed. Activate with: .\\venv\\Scripts\\Activate.ps1"

