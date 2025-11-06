import pytest
from fastapi.testclient import TestClient
from api.main import app
from database.models import init_db
import io
from PIL import Image

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database"""
    init_db()

def create_test_image():
    """Create a test image in memory"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_report_issue_endpoint():
    """Test the main report issue endpoint"""
    image = create_test_image()
    
    response = client.post(
        "/api/report-issue",
        files={"image": ("test.jpg", image, "image/jpeg")},
        data={
            "reporter_name": "Test User",
            "location": "Test Location",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "audio_text": "Test audio description"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_get_issues_endpoint():
    """Test getting all issues"""
    response = client.get("/api/issues")
    
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert isinstance(data["issues"], list)

def test_get_specific_issue():
    """Test getting specific issue"""
    # First create an issue
    image = create_test_image()
    
    create_response = client.post(
        "/api/report-issue",
        files={"image": ("test.jpg", image, "image/jpeg")},
        data={
            "reporter_name": "Test User",
            "location": "Test Location"
        }
    )
    
    if create_response.status_code == 200:
        issue_id = create_response.json().get("issue_id")
        
        if issue_id:
            response = client.get(f"/api/issues/{issue_id}")
            assert response.status_code == 200

def test_missing_required_fields():
    """Test API with missing fields"""
    response = client.post(
        "/api/report-issue",
        data={"reporter_name": "Test User"}
    )
    
    assert response.status_code == 422  # Validation error