# Code Live - Troubleshooting Guide

## 🎛️ **Push-Proof System Troubleshooting**

### **🔧 Common Issues and Quick Fixes**

#### **1. Hook didn't run**
```bash
# Symptoms: Pre-commit hooks not executing
# Fix: Reinstall hooks
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit run --all-files
```

#### **2. Can't push to main**
```bash
# Symptoms: "Push to main blocked" error
# Fix: Use feature branch workflow
git checkout -b feature/your-feature
git push origin feature/your-feature
gh pr create --title "Your Feature" --body "Description"
```

#### **3. Large file blocked**
```bash
# Symptoms: "File exceeds 100MB" error
# Fix: Move to Git LFS
git lfs track "*.mp4" "*.mov" "*.zip" "*.pickle" "*.onnx" "*.bin" "*.model"
git add .gitattributes
git add your-large-file.mp4
git commit -m "feat: add large file to LFS"
```

#### **4. Secrets flagged**
```bash
# Symptoms: "Secret detected" error
# Fix: Remove from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret' \
  --prune-empty --tag-name-filter cat -- --all
git push --force-with-lease
```

#### **5. Line ending issues**
```bash
# Symptoms: "Changed every line" diffs
# Fix: Normalize line endings
git add --renormalize .
git commit -m "Normalize line endings"
```

#### **6. Pre-commit configuration errors**
```bash
# Symptoms: "InvalidManifestError" or hook failures
# Fix: Update pre-commit configuration
pre-commit autoupdate
pre-commit run --all-files
```

#### **7. Git LFS not working**
```bash
# Symptoms: Large files not tracked in LFS
# Fix: Verify LFS setup
git lfs install
git lfs ls-files --errors
git lfs migrate import --include="*.mp4,*.mov,*.zip,*.pickle,*.onnx,*.bin,*.model"
```

#### **8. CI/CD failures**
```bash
# Symptoms: GitHub Actions failing
# Fix: Check local hooks first
pre-commit run --all-files
pytest -q
mypy pcs/ --ignore-missing-imports
```

#### **9. Branch protection issues**
```bash
# Symptoms: "Protected branch hook declined"
# Fix: Check required status checks
gh api repos/TUNEZILLA-zz/polygot-code-sampler/branches/main/protection
# Ensure all required checks are passing
```

#### **10. Authentication issues**
```bash
# Symptoms: "Authentication failed" or "403" errors
# Fix: Use SSH or PAT with repo scope
git remote set-url origin git@github.com:TUNEZILLA-zz/polygot-code-sampler.git
ssh -T git@github.com
```

### **🔍 Diagnostic Commands**

#### **Check Git configuration**
```bash
git remote -v
git status
git config --get remote.origin.url
```

#### **Check for large files**
```bash
git ls-files | xargs -I{} sh -c 'test -f {} && echo $(stat -c%s {}) {}' | sort -nr | head -10
```

#### **Check for secrets**
```bash
grep -r "sk-" . --exclude-dir=.git --exclude-dir=node_modules
grep -r "AKIA" . --exclude-dir=.git --exclude-dir=node_modules
```

#### **Check Git LFS status**
```bash
git lfs ls-files
git lfs ls-files --errors
```

#### **Check pre-commit status**
```bash
pre-commit --version
pre-commit run --all-files
```

### **🚨 Emergency Procedures**

#### **Force push (DANGER - use with caution)**
```bash
# Only if absolutely necessary and you understand the risks
git push --force-with-lease origin your-branch
```

#### **Reset to clean state**
```bash
# Reset to last known good commit
git reset --hard HEAD~1
git push --force-with-lease origin your-branch
```

#### **Bypass hooks (NOT RECOMMENDED)**
```bash
# Only for emergency fixes
git commit --no-verify -m "emergency: bypass hooks"
```

### **📞 Getting Help**

#### **Check logs**
```bash
# Pre-commit logs
cat ~/.cache/pre-commit/pre-commit.log

# Git logs
git log --oneline -10

# CI logs
gh run list
gh run view <run-id>
```

#### **Contact support**
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and help
- **Team members**: For urgent issues

### **🛠️ Advanced Troubleshooting**

#### **Clean environment**
```bash
# Remove all cached environments
pre-commit clean
pre-commit install --hook-type pre-commit --hook-type pre-push
```

#### **Update all tools**
```bash
# Update pre-commit hooks
pre-commit autoupdate

# Update Python dependencies
pip install --upgrade -r requirements.txt

# Update Node.js dependencies
npm update
```

#### **Reset Git configuration**
```bash
# Reset to default configuration
git config --unset-all remote.origin.url
git remote set-url origin https://github.com/TUNEZILLA-zz/polygot-code-sampler.git
```

### **✅ Verification Checklist**

Before pushing, ensure:
- [ ] All pre-commit hooks pass
- [ ] No large files (>100MB)
- [ ] No secrets in code
- [ ] Line endings normalized
- [ ] Git LFS properly configured
- [ ] Feature branch created (not pushing to main)
- [ ] Commit message follows convention
- [ ] Tests pass locally

### **🎯 Quick Reference**

| Issue | Command | Description |
|-------|---------|-------------|
| Hooks not running | `pre-commit install` | Reinstall pre-commit hooks |
| Can't push to main | `git checkout -b feature/name` | Create feature branch |
| Large file blocked | `git lfs track "*.ext"` | Track file in LFS |
| Secrets detected | `git filter-branch` | Remove from history |
| Line ending issues | `git add --renormalize .` | Normalize line endings |
| CI failing | `pre-commit run --all-files` | Check local hooks first |

---

*Remember: The push-proof system is designed to help, not hinder. When in doubt, ask for help! 🎛️✨*
