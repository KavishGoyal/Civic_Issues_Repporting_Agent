from groq import Groq
import os
import json
from typing import Dict, Any
from database.models import Agency, Notification, SessionLocal
from dotenv import load_dotenv
load_dotenv()

class NotificationAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def route_to_agency(self, issue_type: str) -> Dict[str, Any]:
        """Route issue to appropriate agency"""
        db = SessionLocal()
        
        agencies = db.query(Agency).all()
        
        for agency in agencies:
            if issue_type in agency.issue_types:
                db.close()
                return {
                    "agency_id": agency.id,
                    "agency_name": agency.name,
                    "email": agency.email,
                    "phone": agency.phone
                }
        
        db.close()
        return None
    
    def generate_notification(self, issue_data: Dict) -> str:
        """Generate professional notification message for agency"""
        
        prompt = f"""Create a professional notification message for a civic agency:

Reporter: {issue_data['reporter_name']}
Location: {issue_data['location']}
Issue Type: {issue_data['issue_type']}
Description: {issue_data['description']}
Severity: {issue_data['severity']}

Create a concise, professional message (max 200 words) that includes:
1. Brief summary
2. Exact location
3. Severity level
4. Immediate action required

Make it actionable and urgent without being alarmist."""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=512
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating notification: {e}")
            return f"URGENT: {issue_data['issue_type'].upper()} reported at {issue_data['location']} by {issue_data['reporter_name']}. {issue_data['description']}"
    
    def send_notification(self, issue_id: int, agency_data: Dict, message: str) -> bool:
        """Send notification to agency (simulate email/SMS)"""
        db = SessionLocal()
        
        notification = Notification(
            issue_id=issue_id,
            agency_id=agency_data['agency_id'],
            message=message,
            status="sent"
        )
        
        db.add(notification)
        db.commit()
        
        # In production, integrate with email/SMS service
        print(f"\n{'='*60}")
        print(f"NOTIFICATION SENT TO: {agency_data['agency_name']}")
        print(f"Email: {agency_data['email']}")
        print(f"Phone: {agency_data['phone']}")
        print(f"\nMessage:\n{message}")
        print(f"{'='*60}\n")
        
        db.close()
        return True