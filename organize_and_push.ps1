# Script to organize Oracle Knowledge Graph project and push to GitHub

Write-Host "Organizing Oracle Knowledge Graph Project" -ForegroundColor Cyan
Write-Host "=" * 60

# 1. Pull existing files from GitHub
Write-Host "`nStep 1: Pulling existing files from GitHub..." -ForegroundColor Yellow
git pull origin knowledge_graph --allow-unrelated-histories

# 2. Create project folder
Write-Host "`nStep 2: Creating oracle-knowledge-graph folder..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "oracle-knowledge-graph" -Force | Out-Null

# 3. Move project files
Write-Host "`nStep 3: Moving project files..." -ForegroundColor Yellow

# Folders to move
$folders = @("src", "notebooks", "files", "data")
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "  Moving $folder..."
        Move-Item -Path $folder -Destination "oracle-knowledge-graph\" -Force -ErrorAction SilentlyContinue
    }
}

# Documentation files
$docFiles = @(
    "ARCHITECTURE.md",
    "GET_STARTED.md", 
    "INSTALL_WINDOWS.md",
    "PROJECT_STRUCTURE.md",
    "QUICK_REFERENCE.md",
    "TROUBLESHOOTING.md",
    "WINDOWS_SETUP.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Write-Host "  Moving $file..."
        Move-Item -Path $file -Destination "oracle-knowledge-graph\" -Force -ErrorAction SilentlyContinue
    }
}

# Configuration files
$configFiles = @(
    "docker-compose.yml",
    "requirements.txt",
    "requirements-minimal.txt",
    ".env.example",
    ".gitignore"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "  Moving $file..."
        Move-Item -Path $file -Destination "oracle-knowledge-graph\" -Force -ErrorAction SilentlyContinue
    }
}

# Python scripts
Write-Host "  Moving Python scripts..."
Get-ChildItem -Path . -Filter "*.py" -File | ForEach-Object {
    if ($_.Name -ne "organize_and_push.ps1") {
        Move-Item -Path $_.FullName -Destination "oracle-knowledge-graph\" -Force -ErrorAction SilentlyContinue
    }
}

# PowerShell scripts (except this one)
Get-ChildItem -Path . -Filter "*.ps1" -File | ForEach-Object {
    if ($_.Name -ne "organize_and_push.ps1") {
        Move-Item -Path $_.FullName -Destination "oracle-knowledge-graph\" -Force -ErrorAction SilentlyContinue
    }
}

# 4. Remove venv if it was moved (too large for git)
if (Test-Path "oracle-knowledge-graph\venv") {
    Write-Host "`nStep 4: Removing venv folder (too large for git)..." -ForegroundColor Yellow
    Remove-Item -Path "oracle-knowledge-graph\venv" -Recurse -Force -ErrorAction SilentlyContinue
}

# 5. Remove oracle-metadata-knowledge-graph folder if it exists
if (Test-Path "oracle-metadata-knowledge-graph") {
    Write-Host "`nStep 5: Removing duplicate oracle-metadata-knowledge-graph folder..." -ForegroundColor Yellow
    Remove-Item -Path "oracle-metadata-knowledge-graph" -Recurse -Force -ErrorAction SilentlyContinue
}

# 6. Show structure
Write-Host "`nStep 6: New structure:" -ForegroundColor Yellow
Write-Host "Root directory:"
Get-ChildItem -Path . -Exclude .git | Select-Object Name, Mode

Write-Host "`noracle-knowledge-graph directory:"
Get-ChildItem -Path "oracle-knowledge-graph" | Select-Object Name, Mode | Format-Table

# 7. Stage changes
Write-Host "`nStep 7: Staging changes..." -ForegroundColor Yellow
git add .

# 8. Show what will be committed
Write-Host "`nFiles to be committed:" -ForegroundColor Cyan
git status --short

# 9. Commit
Write-Host "`nStep 8: Committing changes..." -ForegroundColor Yellow
git commit -m "Organize: Move Oracle Knowledge Graph to dedicated folder

- Created oracle-knowledge-graph/ folder
- Moved all project files to subfolder
- Added comprehensive README
- Preserved existing repository files"

# 10. Push
Write-Host "`nStep 9: Pushing to GitHub..." -ForegroundColor Yellow
git push origin knowledge_graph

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n" + "=" * 60 -ForegroundColor Green
    Write-Host "Success! Project organized and uploaded" -ForegroundColor Green
    Write-Host "View at: https://github.com/veeramani5034/GenAI/tree/knowledge_graph/oracle-knowledge-graph" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Green
} else {
    Write-Host "`nError: Push failed" -ForegroundColor Red
}

# Cleanup this script
Write-Host "`nCleaning up..." -ForegroundColor Yellow
Remove-Item -Path "organize_and_push.ps1" -Force -ErrorAction SilentlyContinue
