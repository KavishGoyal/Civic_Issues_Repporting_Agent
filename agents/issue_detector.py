import base64
from groq import Groq
import os
import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()
class IssueDetectorAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def detect_issue(self, image_path: str, audio_text: str = None) -> Dict[str, Any]:
        """Detect civic issues from image and audio using Groq Vision"""
        
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = """Analyze this image and identify any civic issues present. Look for:
- Water leaks, broken pipes, or unnecessary water flow
- Garbage, litter, or unpicked waste
- Potholes or road damage
- Dirt or debris on roads
- Any visible criminal or suspicious activity
- Any issue or accident

Respond in JSON format with:
{
    "issue_detected": true/false,
    "issue_type": "water_leak|garbage|pothole|criminal_activity|dirt_on_road|accident/none",
    "severity": "low|medium|high|critical",
    "description": "detailed description",
    "confidence": 0.0-1.0
}"""

        if audio_text:
            prompt += f"\n\nAdditional context from audio: {audio_text}"
        
        try:
            response = self.groq_client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )
            raw_message = response.choices[0].message.content.strip()
            print("Vision Agent Response:", raw_message)
            cleaned = re.sub(r"^```(?:json)?|```$", "", raw_message, flags=re.MULTILINE).strip()
            result = json.loads(cleaned)
            print("Vision Agent:", result)
            return result
            
        except Exception as e:
            print(f"Error in issue detection: {e}")
            return {
                "issue_detected": False,
                "issue_type": "none",
                "severity": "low",
                "description": "Error in detection",
                "confidence": 0.0
            }