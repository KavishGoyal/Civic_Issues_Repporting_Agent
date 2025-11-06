echo "Starting Civic Issue Detection System..."
echo "========================================"

# Create necessary directories
mkdir -p uploads
mkdir -p logs

# Start PostgreSQL (assuming it's installed and configured)
echo "Starting PostgreSQL..."
# sudo service postgresql start

# Initialize database
echo "Initializing database..."
python database/seed_data.py

# Start MCP Server
echo "Starting MCP Server on port 8001..."
python mcp/server.py > logs/mcp.log 2>&1 &
MCP_PID=$!

# Wait for MCP to start
sleep 3

# Start FastAPI Server
echo "Starting FastAPI Server on port 8000..."
python app/main.py > logs/api.log 2>&1 &
API_PID=$!

# Wait for API to start
sleep 3

# Start Streamlit App
echo "Starting Streamlit App on port 8501..."
streamlit run streamlit_app.py > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!

echo ""
echo "========================================"
echo "All services started successfully!"
echo "========================================"
echo "MCP Server:     http://localhost:8001"
echo "FastAPI:        http://localhost:8000"
echo "Streamlit UI:   http://localhost:8501"
echo "API Docs:       http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Process IDs:"
echo "MCP PID: $MCP_PID"
echo "API PID: $API_PID"
echo "Streamlit PID: $STREAMLIT_PID"
echo ""
echo "To stop all services, run: ./stop_services.sh"
echo "Or press Ctrl+C and then run: kill $MCP_PID $API_PID $STREAMLIT_PID"

# Keep script running
wait