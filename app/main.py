from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.models import CivicIssue, get_db, init_db
from agents.orchestrator import CivicAgentOrchestrator, AgentState
import shutil
from pathlib import Path
import uvicorn
from datetime import datetime

app = FastAPI(title="Civic Issue Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

orchestrator = CivicAgentOrchestrator()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/api/report-issue")
async def report_issue(
    image: UploadFile = File(...),
    reporter_name: str = Form(...),
    location: str = Form(...),
    latitude: float = Form(None),
    longitude: float = Form(None),
    audio_text: str = Form(None),
    db: Session = Depends(get_db)
):
    """Main endpoint to report civic issues"""
    
    # Save uploaded image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = UPLOAD_DIR / f"{timestamp}_{image.filename}"
    
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Process through agent workflow
    initial_state: AgentState = {
        "image_path": str(image_path),
        "audio_text": audio_text,
        "reporter_name": reporter_name,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
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
    
    result = orchestrator.process(initial_state)
    print("Agents Results:",result)
    if not result["issue_detected"]:
        return {
            "status": "no_issue",
            "message": "No significant civic issue detected in the image",
            "confidence": result["confidence"]
        }
    
    # Save to database
    issue = CivicIssue(
        reporter_name=reporter_name,
        location=location,
        latitude=latitude,
        longitude=longitude,
        issue_type=result["issue_type"],
        description=result["description"],
        image_path=str(image_path),
        audio_path=audio_text,
        status="reported",
        priority=result["severity"],
        assigned_agency=result["agency_data"].get("agency_name") if result["agency_data"] else None,
        suggested_actions=result["suggested_actions"]
    )
    
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # Send notification with correct issue_id
    if result["agency_data"]:
        issue_data = {
            "reporter_name": reporter_name,
            "location": location,
            "issue_type": result["issue_type"],
            "description": result["description"],
            "severity": result["severity"]
        }
        message = orchestrator.notifier.generate_notification(issue_data)
        orchestrator.notifier.send_notification(issue.id, result["agency_data"], message)
    
    return {
        "status": "success",
        "issue_id": issue.id,
        "issue_type": result["issue_type"],
        "severity": result["severity"],
        "description": result["description"],
        "suggested_actions": result["suggested_actions"],
        "agency_notified": result["agency_data"].get("agency_name") if result["agency_data"] else None,
        "confidence": result["confidence"]
    }

@app.get("/api/issues")
async def get_issues(db: Session = Depends(get_db)):
    """Get all reported issues"""
    issues = db.query(CivicIssue).order_by(CivicIssue.created_at.desc()).all()
    return {"issues": issues}

@app.get("/api/issues/{issue_id}")
async def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get specific issue details"""
    issue = db.query(CivicIssue).filter(CivicIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)