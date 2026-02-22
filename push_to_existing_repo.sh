#!/bin/bash

echo "🚀 Pushing to existing GitHub repository..."
echo "Repository: https://github.com/sajalhack/sajalhackthethread.git"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add remote (will update if exists)
echo "🔗 Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/sajalhack/sajalhackthethread.git

# Check what will be committed
echo ""
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
read -p "Create commit? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Add Social Saver Bot: WhatsApp bot that saves Instagram/Twitter links to searchable dashboard"
    echo "✅ Commit created!"
    echo ""
    echo "📤 Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    echo ""
    echo "✅ Done! Check your repository: https://github.com/sajalhack/sajalhackthethread"
else
    echo "ℹ️  Files staged but not committed. Run 'git commit' when ready."
fi
