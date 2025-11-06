import pytest
from fastapi.testclient import TestClient
from mcp.server import app

client = TestClient(app)

def test_mcp_health_check():
    """Test MCP server health"""
    response = client.get("/mcp/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_mcp_context_endpoint():
    """Test MCP context provision"""
    response = client.post(
        "/mcp/context",
        json={
            "context_type": "issue_detection",
            "data": {"test": "data"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "context" in data