from groq import Groq
import os
import json
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()

class ActionPlannerAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def suggest_actions(self, issue_type: str, description: str, severity: str) -> List[Dict[str, str]]:
        """Generate actionable suggestions for the detected issue"""
        
        prompt = f"""As a civic management expert, provide actionable suggestions for this issue:

Issue Type: {issue_type}
Description: {description}
Severity: {severity}

Provide 3-5 immediate actions that:
1. Citizens can take
2. Local authorities should take
3. Preventive measures for future

Respond in JSON format:
{{
    "immediate_actions": ["action1", "action2", ...],
    "citizen_actions": ["action1", "action2", ...],
    "authority_actions": ["action1", "action2", ...],
    "preventive_measures": ["measure1", "measure2", ...]
}}"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1024
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error in action planning: {e}")
            return {
                "immediate_actions": ["Report to authorities", "Document the issue"],
                "citizen_actions": ["Stay safe", "Inform neighbors"],
                "authority_actions": ["Inspect the site", "Deploy team"],
                "preventive_measures": ["Regular maintenance", "Community awareness"]
            }