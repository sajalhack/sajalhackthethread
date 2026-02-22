#!/bin/bash

echo "🚀 Preparing to push to GitHub..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Check what will be committed
echo "📋 Checking files to be committed..."
git status

echo ""
echo "⚠️  IMPORTANT: Make sure config.py is NOT in the list above!"
echo "   If you see config.py, it will expose your API keys!"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted. Please check .gitignore first."
    exit 1
fi

# Add all files
echo "➕ Adding files..."
git add .

# Show what's staged
echo ""
echo "📦 Files staged for commit:"
git status --short

echo ""
read -p "Create initial commit? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Initial commit: Social Saver Bot - WhatsApp bot that saves Instagram links to searchable dashboard"
    echo "✅ Commit created!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Create a new repository on GitHub: https://github.com/new"
    echo "2. Copy the repository URL"
    echo "3. Run these commands:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
else
    echo "ℹ️  Files staged but not committed. Run 'git commit' when ready."
fi
