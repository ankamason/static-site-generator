#!/bin/bash

echo "🚀 Building static site for GitHub Pages deployment..."

# Replace YOUR_REPO_NAME with your actual GitHub repository name
REPO_NAME="static-site-generator"

echo "📝 Building site with basepath: /static_site_generator/"
echo "🎯 Output directory: docs/"

# Build the site for production with the correct basepath
python3 src/main.py "/static-site-generator/"

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Production build completed successfully!"
    echo "📁 Site built in docs/ directory"
    echo "🔗 Configured for GitHub Pages URL: https://ankamason.github.io/static-site-generator/"
    echo ""
    echo "Next steps:"
    echo "1. Commit and push the docs/ directory to GitHub"
    echo "2. Enable GitHub Pages in repository settings"
    echo "3. Set source to 'main branch' and 'docs' folder"
else
    echo "❌ Production build failed!"
    exit 1
fi
