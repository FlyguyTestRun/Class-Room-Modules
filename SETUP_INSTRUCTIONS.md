# 🚀 EduOps Command Center - Setup Instructions

**Welcome!** This package contains everything you need to initialize your EduOps Command Center repository.

---

## 📦 Package Contents

You should have these files:

1. ✅ **Initialize-EduOpsRepo.ps1** - Main setup script
2. ✅ **TODO.md** - Complete task breakdown
3. ✅ **INTERVIEW_PREP.md** - Keller ISD interview Q&A
4. ✅ **PORTFOLIO_PRESENTATION.md** - 10-minute demo script
5. ✅ **LINKEDIN_POST.md** - Professional announcement guide
6. ✅ **SETUP_INSTRUCTIONS.md** - This file

---

## ⚡ Quick Start (Windows)

### Step 1: Navigate to Your Repo Directory

```powershell
# If you haven't cloned yet:
cd C:\Projects  # or wherever you store code
git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git
cd Class-Room-Modules

# If you already have it cloned:
cd C:\Projects\Class-Room-Modules
```

### Step 2: Copy Setup Files

Copy all files from this package into your repo directory:

```powershell
# Copy the setup files to your repo
Copy-Item "C:\Downloads\eduops-setup\*" -Destination . -Recurse
```

### Step 3: Run the Setup Script

```powershell
# Allow script execution (one-time, if needed)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run the initialization script
.\Initialize-EduOpsRepo.ps1
```

The script will:
- Create all folder structures
- Generate configuration files
- Initialize Git (if not already)
- Stage and commit files

### Step 4: Push to GitHub

```powershell
# If remote not set:
git remote add origin https://github.com/FlyguyTestRun/Class-Room-Modules.git

# Push to GitHub
git push -u origin main
```

---

## 🐧 Quick Start (Linux/Mac)

### Step 1: Install PowerShell (if needed)

```bash
# Mac (using Homebrew)
brew install --cask powershell

# Ubuntu/Debian
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y powershell

# Verify installation
pwsh --version
```

### Step 2: Navigate and Copy Files

```bash
# Clone repo if you haven't
cd ~/Projects
git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git
cd Class-Room-Modules

# Copy setup files
cp -r ~/Downloads/eduops-setup/* .
```

### Step 3: Run Setup Script

```bash
# Launch PowerShell
pwsh

# Run the script
./Initialize-EduOpsRepo.ps1

# Exit PowerShell when done
exit
```

### Step 4: Push to GitHub

```bash
git remote add origin https://github.com/FlyguyTestRun/Class-Room-Modules.git
git push -u origin main
```

---

## 📝 What the Script Creates

### Folder Structure (70+ directories)
```
Class-Room-Modules/
├── automation/          # PowerShell & Python automation
├── docker/              # Container configurations
├── infrastructure/      # Terraform, Cloudshare, databases
├── ai_components/       # RAG, MCP servers, knowledge base
├── training/            # 7 training modules
├── monitoring/          # Grafana, Prometheus
├── docs/                # Architecture, API docs
├── tests/               # Unit, integration, E2E tests
└── .github/             # Workflows, issue templates
```

### Configuration Files
- `.gitignore` - Excludes secrets, temp files
- `.env.template` - Environment variables template
- `README.md` - Portfolio-ready project description
- `docker-compose.yml` (placeholder - you'll build this)

### Documentation Files
- `PROJECT_SCOPE.md` (you'll create this next with first FILE content from earlier)
- `TODO.md` ✅ (already created)
- `INTERVIEW_PREP.md` ✅ (already created)
- `PORTFOLIO_PRESENTATION.md` ✅ (already created)
- `LINKEDIN_POST.md` ✅ (already created)

---

## 🔧 Post-Setup Steps

### 1. Create Additional Documentation

The setup script created the folder structure. Now add the main documentation files:

**Copy these from earlier in our conversation:**
- `PROJECT_SCOPE.md` - The comprehensive portfolio version
- `INSTRUCTOR_GUIDE.md` - Teaching materials
- `GITHUB_SETUP.md` - Git workflow guide
- `FUTURE_ENHANCEMENTS.md` - Roadmap

**Quick command to create placeholders:**

```powershell
# Create placeholder files
@"
# Coming Soon
This file will contain [description].
"@ | Out-File -FilePath "PROJECT_SCOPE.md" -Encoding UTF8

# Do the same for other files...
```

### 2. Configure Environment Variables

```powershell
# Copy the template
Copy-Item .env.template .env

# Edit with your values
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Required values:**
- `CLAUDE_API_KEY` - Get from console.anthropic.com
- `DB_PASSWORD` - Generate secure password
- `REDIS_PASSWORD` - Generate secure password
- `API_SECRET_KEY` - Generate random string

### 3. Verify Git Status

```powershell
git status
# Should show clean working directory

git log --oneline
# Should show: "Initial commit: EduOps Command Center..."
```

### 4. Start Building

Follow the **TODO.md** file:
- Phase 0: Foundation (setup complete! ✅)
- Phase 1: Docker Infrastructure (next step)
- Phase 2: PowerShell Automation
- ... continue through phases

---

## 🆘 Troubleshooting

### "Execution policy" error

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### "Git not found" error

Install Git:
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`
- Linux: `sudo apt-get install git`

### "Permission denied" errors (Linux/Mac)

```bash
chmod +x Initialize-EduOpsRepo.ps1
```

### Script creates files but doesn't commit

```powershell
# Manual git setup
git init
git add .
git commit -m "Initial commit: EduOps Command Center repository structure and documentation"
git branch -M main
git remote add origin https://github.com/FlyguyTestRun/Class-Room-Modules.git
git push -u origin main
```

### Docker not found

Install Docker Desktop:
- Windows/Mac: https://www.docker.com/products/docker-desktop/
- Linux: https://docs.docker.com/engine/install/

---

## 📚 Next Steps

### 1. Read the Documentation
- **TODO.md** - Your development roadmap
- **INTERVIEW_PREP.md** - Prepare for Keller ISD
- **PORTFOLIO_PRESENTATION.md** - Practice your demo

### 2. Set Up Cloudshare Lab
Follow instructions in `TODO.md` Phase 0

### 3. Start Building with Claude Code
```bash
# Open in VS Code
code .

# Start with Phase 1: Docker Infrastructure
# Use TODO.md as your guide
```

### 4. Commit Frequently
```powershell
git add .
git commit -m "feat: Add PowerShell identity module"
git push
```

---

## 🎯 Success Criteria

You're ready to proceed when:
- [ ] All folders created (70+ directories)
- [ ] Git initialized and pushed to GitHub
- [ ] `.env` file configured with credentials
- [ ] Documentation files present
- [ ] README displays correctly on GitHub
- [ ] TODO.md loaded in your task tracker

---

## 📞 Need Help?

**For setup issues:**
- Check troubleshooting section above
- Review PowerShell script output for errors
- Ensure all prerequisites installed (Git, Docker, PowerShell)

**For development questions:**
- Use Claude Code with TODO.md as reference
- Reference INSTRUCTOR_GUIDE.md for detailed explanations
- Check GitHub Issues in your repo

**For interview prep:**
- Review INTERVIEW_PREP.md thoroughly
- Practice demo with PORTFOLIO_PRESENTATION.md
- Time yourself (target: 10 minutes)

---

## 🎉 Congratulations!

Your EduOps Command Center repository is initialized and ready for development.

**Remember:**
- This is production-grade work - take your time
- Document as you go
- Commit frequently with clear messages
- Follow the TODO.md phase-by-phase
- Ask Claude Code for help when stuck

**You've got this! 🚀**

---

*Setup Instructions v1.0 - January 2026*
