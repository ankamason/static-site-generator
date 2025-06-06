python3 src/main.py
#!/bin/bash

echo "🚀 Building static site and starting development server..."

# Generate the static site
echo "📝 Generating static site..."
python3 src/main.py

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo "✅ Site generation completed successfully!"
    echo "🌐 Starting development server on http://localhost:8888"
    echo "📡 Press Ctrl+C to stop the server"
    echo ""
    
    # Start the web server in the public directory
    cd public && python3 -m http.server 8888 --bind 127.0.0.1
else
    echo "❌ Site generation failed!"
    exit 1
fi
