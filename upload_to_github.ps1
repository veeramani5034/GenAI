# Upload Oracle Knowledge Graph to GitHub
# Run this script to push your project to GitHub

Write-Host "Oracle Metadata Knowledge Graph - GitHub Upload" -ForegroundColor Cyan
Write-Host "=" * 60

# Check if git is installed
try {
    git --version | Out-Null
} catch {
    Write-Host "Error: Git is not installed" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win"
    exit 1
}

Write-Host "`nStep 1: Checking git configuration..." -ForegroundColor Yellow

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..."
    git init
}

# Check git config
$userName = git config user.name
$userEmail = git config user.email

if (-not $userName -or -not $userEmail) {
    Write-Host "`nGit user not configured. Please enter your details:" -ForegroundColor Yellow
    $userName = Read-Host "Enter your name"
    $userEmail = Read-Host "Enter your email"
    
    git config user.name $userName
    git config user.email $userEmail
    Write-Host "Git configured successfully!" -ForegroundColor Green
}

Write-Host "`nStep 2: Setting up remote repository..." -ForegroundColor Yellow

# Add or update remote
$remoteUrl = "https://github.com/veeramani5034/GenAI.git"
$remoteExists = git remote get-url origin 2>$null

if ($remoteExists) {
    Write-Host "Updating remote URL..."
    git remote set-url origin $remoteUrl
} else {
    Write-Host "Adding remote repository..."
    git remote add origin $remoteUrl
}

Write-Host "`nStep 3: Fetching remote branches..." -ForegroundColor Yellow
git fetch origin

Write-Host "`nStep 4: Switching to knowledge_graph branch..." -ForegroundColor Yellow

# Check if branch exists locally
$branchExists = git branch --list knowledge_graph

if ($branchExists) {
    git checkout knowledge_graph
} else {
    # Check if branch exists on remote
    $remoteBranchExists = git branch -r --list origin/knowledge_graph
    
    if ($remoteBranchExists) {
        git checkout -b knowledge_graph origin/knowledge_graph
    } else {
        git checkout -b knowledge_graph
    }
}

Write-Host "`nStep 5: Staging files..." -ForegroundColor Yellow
git add .

Write-Host "`nFiles to be committed:" -ForegroundColor Cyan
git status --short

Write-Host "`n" + "=" * 60
$confirm = Read-Host "Do you want to commit and push these files? (y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "`nStep 6: Committing changes..." -ForegroundColor Yellow
    
    $commitMessage = Read-Host "Enter commit message (or press Enter for default)"
    
    if (-not $commitMessage) {
        $commitMessage = "Add Oracle Metadata to Neo4j Knowledge Graph project"
    }
    
    git commit -m $commitMessage
    
    Write-Host "`nStep 7: Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host "Note: You may need to enter your GitHub username and Personal Access Token" -ForegroundColor Cyan
    
    git push -u origin knowledge_graph
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n" + "=" * 60 -ForegroundColor Green
        Write-Host "Success! Project uploaded to GitHub" -ForegroundColor Green
        Write-Host "View at: https://github.com/veeramani5034/GenAI/tree/knowledge_graph" -ForegroundColor Cyan
        Write-Host "=" * 60 -ForegroundColor Green
    } else {
        Write-Host "`nError: Push failed" -ForegroundColor Red
        Write-Host "If authentication failed, you need a Personal Access Token:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://github.com/settings/tokens"
        Write-Host "2. Generate new token (classic)"
        Write-Host "3. Select 'repo' scope"
        Write-Host "4. Use token as password when prompted"
    }
} else {
    Write-Host "`nUpload cancelled" -ForegroundColor Yellow
}
