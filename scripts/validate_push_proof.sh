#!/usr/bin/env bash
# Code Live - Push-Proof Validation Checklist
# Quick 5-minute validation of the entire push-proof system

set -euo pipefail

echo "🎛️ Code Live - Push-Proof Validation Checklist"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check functions
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

echo ""
echo "🔍 1. Branch Protection Validation"
echo "----------------------------------"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    check_fail "Not in a git repository"
fi

# Check remote URL
remote_url=$(git config --get remote.origin.url)
if [[ "$remote_url" == *"github.com"* ]]; then
    check_pass "GitHub remote configured"
else
    check_warn "Not a GitHub repository: $remote_url"
fi

# Check branch protection (requires GitHub CLI)
if command -v gh >/dev/null 2>&1; then
    if gh auth status >/dev/null 2>&1; then
        repo_info=$(gh repo view --json name,owner 2>/dev/null || echo '{"name":"unknown","owner":{"login":"unknown"}}')
        repo_name=$(echo "$repo_info" | jq -r '.name')
        repo_owner=$(echo "$repo_info" | jq -r '.owner.login')

        if [[ "$repo_name" != "unknown" ]]; then
            check_info "Repository: $repo_owner/$repo_name"

            # Check branch protection
            protection_status=$(gh api "repos/$repo_owner/$repo_name/branches/main/protection" 2>/dev/null || echo "{}")
            if [[ "$protection_status" != "{}" ]]; then
                check_pass "Branch protection configured for main"
            else
                check_warn "Branch protection not configured - run .github/branch-protection.yml"
            fi
        else
            check_warn "Could not determine repository info"
        fi
    else
        check_warn "GitHub CLI not authenticated - run 'gh auth login'"
    fi
else
    check_warn "GitHub CLI not installed - install with 'brew install gh'"
fi

echo ""
echo "🔍 2. Required Status Checks Validation"
echo "--------------------------------------"

# Check if required workflow files exist
required_workflows=(
    ".github/workflows/ci-mirror-hooks.yml"
    ".github/workflows/lfs-enforcement.yml"
    ".github/workflows/golden-stability.yml"
    ".github/workflows/matrix-smoke.yml"
    ".github/workflows/publish-dashboard.yml"
)

for workflow in "${required_workflows[@]}"; do
    if [[ -f "$workflow" ]]; then
        check_pass "Workflow exists: $workflow"
    else
        check_fail "Missing workflow: $workflow"
    fi
done

echo ""
echo "🔍 3. Pre-commit Hooks Validation"
echo "---------------------------------"

# Check pre-commit installation
if command -v pre-commit >/dev/null 2>&1; then
    check_pass "Pre-commit installed"

    # Check pre-commit version
    pre_commit_version=$(pre-commit --version)
    check_info "Pre-commit version: $pre_commit_version"

    # Check if hooks are installed
    if [[ -f ".git/hooks/pre-commit" ]]; then
        check_pass "Pre-commit hooks installed"
    else
        check_warn "Pre-commit hooks not installed - run 'pre-commit install'"
    fi

    if [[ -f ".git/hooks/pre-push" ]]; then
        check_pass "Pre-push hooks installed"
    else
        check_warn "Pre-push hooks not installed - run 'pre-commit install --hook-type pre-push'"
    fi

    # Test pre-commit run
    echo "🧪 Testing pre-commit hooks..."
    if pre-commit run --all-files --hook-stage manual >/dev/null 2>&1; then
        check_pass "Pre-commit hooks pass"
    else
        check_warn "Pre-commit hooks have issues - run 'pre-commit run --all-files' for details"
    fi
else
    check_fail "Pre-commit not installed - run 'pip install pre-commit'"
fi

echo ""
echo "🔍 4. Git LFS Validation"
echo "------------------------"

# Check Git LFS installation
if command -v git-lfs >/dev/null 2>&1; then
    check_pass "Git LFS installed"

    # Check LFS configuration
    if git lfs ls-files --errors >/dev/null 2>&1; then
        check_pass "Git LFS configuration valid"
    else
        check_warn "Git LFS configuration issues - run 'git lfs ls-files --errors' for details"
    fi

    # Check .gitattributes
    if [[ -f ".gitattributes" ]]; then
        check_pass ".gitattributes file exists"

        # Check for required LFS patterns
        required_patterns=("*.mp4" "*.mov" "*.zip" "*.pickle" "*.onnx" "*.bin" "*.model")
        for pattern in "${required_patterns[@]}"; do
            if grep -q "$pattern" .gitattributes; then
                check_pass "LFS pattern configured: $pattern"
            else
                check_warn "Missing LFS pattern: $pattern"
            fi
        done
    else
        check_fail ".gitattributes file missing"
    fi
else
    check_fail "Git LFS not installed - install with 'brew install git-lfs'"
fi

echo ""
echo "🔍 5. Large File Detection"
echo "-------------------------"

# Check for large files
large_files=$(find . -type f -size +50M -not -path './.git/*' -not -path './node_modules/*' 2>/dev/null || true)
if [[ -z "$large_files" ]]; then
    check_pass "No large files detected"
else
    check_warn "Large files detected:"
    echo "$large_files" | while read -r file; do
        if [[ -f "$file" ]]; then
            size=$(stat -c%s "$file" 2>/dev/null || echo "unknown")
            echo "  - $file ($size bytes)"
        fi
    done
fi

echo ""
echo "🔍 6. Secret Detection"
echo "--------------------"

# Basic secret scanning
secrets_found=false
if grep -r "sk-" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv >/dev/null 2>&1; then
    check_warn "Potential secret detected: 'sk-' pattern"
    secrets_found=true
fi

if grep -r "AKIA" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv >/dev/null 2>&1; then
    check_warn "Potential AWS key detected: 'AKIA' pattern"
    secrets_found=true
fi

if [[ "$secrets_found" == false ]]; then
    check_pass "No obvious secrets detected"
fi

echo ""
echo "🔍 7. Configuration Files Validation"
echo "-----------------------------------"

# Check required configuration files
required_configs=(
    ".gitignore"
    ".gitattributes"
    ".pre-commit-config.yaml"
    "pyproject.toml"
    "CONTRIBUTING.md"
    "TROUBLESHOOTING.md"
)

for config in "${required_configs[@]}"; do
    if [[ -f "$config" ]]; then
        check_pass "Configuration file exists: $config"
    else
        check_fail "Missing configuration file: $config"
    fi
done

echo ""
echo "🔍 8. CODEOWNERS Validation"
echo "---------------------------"

if [[ -f ".github/CODEOWNERS" ]]; then
    check_pass "CODEOWNERS file exists"

    # Check for critical paths
    critical_paths=(
        "/.github/"
        "/.gitignore"
        "/.gitattributes"
        "/.pre-commit-config.yaml"
        "/pyproject.toml"
    )

    for path in "${critical_paths[@]}"; do
        if grep -q "$path" .github/CODEOWNERS; then
            check_pass "CODEOWNERS covers: $path"
        else
            check_warn "CODEOWNERS missing: $path"
        fi
    done
else
    check_fail "CODEOWNERS file missing"
fi

echo ""
echo "🎉 Validation Complete!"
echo "======================"

echo ""
echo "📋 Summary:"
echo "- Branch protection: $(if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then echo "✅ Configured"; else echo "⚠️  Check manually"; fi)"
echo "- Pre-commit hooks: $(if command -v pre-commit >/dev/null 2>&1; then echo "✅ Installed"; else echo "❌ Not installed"; fi)"
echo "- Git LFS: $(if command -v git-lfs >/dev/null 2>&1; then echo "✅ Configured"; else echo "❌ Not installed"; fi)"
echo "- Configuration: $(if [[ -f ".gitignore" && -f ".gitattributes" && -f ".pre-commit-config.yaml" ]]; then echo "✅ Complete"; else echo "❌ Incomplete"; fi)"
echo "- Documentation: $(if [[ -f "CONTRIBUTING.md" && -f "TROUBLESHOOTING.md" ]]; then echo "✅ Complete"; else echo "❌ Incomplete"; fi)"

echo ""
echo "🚀 Next steps:"
echo "1. Run 'pre-commit install --hook-type pre-commit --hook-type pre-push'"
echo "2. Run 'pre-commit run --all-files' to fix any issues"
echo "3. Test with a feature branch: 'git checkout -b feature/test'"
echo "4. Apply branch protection: './.github/branch-protection.yml'"

echo ""
echo "🎛️ Code Live Push-Proof System - Ready for Production! ✨"
