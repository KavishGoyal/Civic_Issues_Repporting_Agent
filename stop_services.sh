echo "Stopping Civic Issue Detection System..."

# Kill processes by port
kill $(lsof -t -i:8001) 2>/dev/null  # MCP Server
kill $(lsof -t -i:8000) 2>/dev/null  # FastAPI
kill $(lsof -t -i:8501) 2>/dev/null  # Streamlit

echo "All services stopped."