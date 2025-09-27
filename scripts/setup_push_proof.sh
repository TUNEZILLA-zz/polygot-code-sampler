#!/usr/bin/env bash
# Code Live - Push-Proof Setup Script
# Sets up all the tools and configurations to prevent push failures

set -euo pipefail

echo "🎛️ Code Live - Setting up push-proof workflow..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "❌ Not in a git repository. Please run this from the project root."
  exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit >/dev/null 2>&1; then
  echo "📦 Installing pre-commit..."
  if command -v pipx >/dev/null 2>&1; then
    pipx install pre-commit
  elif command -v pip >/dev/null 2>&1; then
    pip install pre-commit
  else
    echo "❌ pip or pipx not found. Please install Python package manager."
    exit 1
  fi
fi

# Initialize pre-commit
echo "🔧 Setting up pre-commit hooks..."
pre-commit install --hook-type pre-commit --hook-type pre-push

# Install Git LFS if not already installed
if ! command -v git-lfs >/dev/null 2>&1; then
  echo "📦 Installing Git LFS..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew >/dev/null 2>&1; then
      brew install git-lfs
    else
      echo "❌ Homebrew not found. Please install Git LFS manually."
      exit 1
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get install git-lfs
    elif command -v yum >/dev/null 2>&1; then
      sudo yum install git-lfs
    else
      echo "❌ Package manager not found. Please install Git LFS manually."
      exit 1
    fi
  else
    echo "❌ Unsupported OS. Please install Git LFS manually."
    exit 1
  fi
fi

# Initialize Git LFS
echo "🔧 Setting up Git LFS..."
git lfs install

# Track large files
echo "📁 Configuring Git LFS tracking..."
git lfs track "*.mp4" "*.mov" "*.zip" "*.pickle" "*.onnx" "*.bin" "*.model"
git add .gitattributes

# Install git-secrets if available
if command -v git-secrets >/dev/null 2>&1; then
  echo "🔍 Setting up git-secrets..."
  git-secrets --install
else
  echo "⚠️  git-secrets not found. Install it for secret scanning."
fi

# Run pre-commit on all files
echo "🧹 Running pre-commit on all files..."
pre-commit run --all-files

echo "✅ Push-proof setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Commit the changes: git add . && git commit -m 'feat: add push-proof configuration'"
echo "2. Push to a feature branch: git push origin feature/your-feature"
echo "3. Open a PR to merge into main"
echo ""
echo "🔒 Protected branches:"
echo "- main: Requires PR and reviews"
echo "- develop: Requires PR and reviews"
echo "- fx-*: Experiment branches (no protection)"
echo ""
echo "📊 Monitoring:"
echo "- Large files: Blocked at 95MB (GitHub limit: 100MB)"
echo "- Secrets: Scanned automatically"
echo "- Formatting: Applied automatically"
echo "- Linting: Checked automatically"
