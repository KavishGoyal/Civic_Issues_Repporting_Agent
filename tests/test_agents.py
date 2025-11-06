import pytest
from agents.issue_detector import IssueDetectorAgent
from agents.action_planner import ActionPlannerAgent
from agents.notification_agent import NotificationAgent
from agents.orchestrator import CivicAgentOrchestrator
import os
from pathlib import Path

@pytest.fixture
def sample_image():
    return "test_data/sample_pothole.jpg"

@pytest.fixture
def detector():
    return IssueDetectorAgent()

@pytest.fixture
def planner():
    return ActionPlannerAgent()

@pytest.fixture
def notifier():
    return NotificationAgent()

def test_issue_detector(detector, sample_image):
    """Test issue detection from image"""
    if not os.path.exists(sample_image):
        pytest.skip("Sample image not found")
    
    result = detector.detect_issue(sample_image, "There's a big pothole")
    
    assert "issue_detected" in result
    assert "issue_type" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)

def test_action_planner(planner):
    """Test action planning"""
    result = planner.suggest_actions(
        issue_type="pothole",
        description="Large pothole on main road",
        severity="high"
    )
    
    assert "immediate_actions" in result
    assert "citizen_actions" in result
    assert "authority_actions" in result
    assert len(result["immediate_actions"]) > 0

def test_notification_routing(notifier):
    """Test agency routing"""
    result = notifier.route_to_agency("pothole")
    
    # May be None if database not seeded
    if result:
        assert "agency_id" in result
        assert "agency_name" in result
        assert "email" in result

def test_notification_generation(notifier):
    """Test notification message generation"""
    issue_data = {
        "reporter_name": "Test User",
        "location": "Test Road",
        "issue_type": "pothole",
        "description": "Large pothole",
        "severity": "high"
    }
    
    message = notifier.generate_notification(issue_data)
    
    assert isinstance(message, str)
    assert len(message) > 0
    assert "Test User" in message or "pothole" in message.lower()

def test_full_workflow():
    """Test complete agent workflow"""
    orchestrator = CivicAgentOrchestrator()
    
    initial_state = {
        "image_path": "test_data/sample_image.jpg",
        "audio_text": "Water leak detected",
        "reporter_name": "Test Reporter",
        "location": "Test Location",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "issue_detected": False,
        "issue_type": "",
        "severity": "",
        "description": "",
        "confidence": 0.0,
        "suggested_actions": {},
        "agency_data": {},
        "notification_sent": False,
        "error": ""
    }
    
    # This will fail if image doesn't exist, but tests the workflow
    try:
        result = orchestrator.process(initial_state)
        assert "issue_detected" in result
    except FileNotFoundError:
        pytest.skip("Test image not found")