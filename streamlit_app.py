import streamlit as st
import requests
from PIL import Image
import io
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Civic Issue Reporter", page_icon="🏙️", layout="wide")

API_URL = "http://localhost:8000"

st.title("🏙️ Civic Issue Detection & Reporting System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    
    try:
        response = requests.get(f"{API_URL}/api/issues")
        if response.status_code == 200:
            issues = response.json()["issues"]
            st.metric("Total Reports", len(issues))
            
            pending = len([i for i in issues if i["status"] == "reported"])
            st.metric("Pending Issues", pending)
            
            high_priority = len([i for i in issues if i["priority"] == "high"])
            st.metric("High Priority", high_priority)
    except:
        st.warning("API not connected")

# Main content
tab1, tab2 = st.tabs(["📝 Report Issue", "📋 View Reports"])

with tab1:
    st.header("Report a Civic Issue")
    
    col1, col2 = st.columns(2)
    
    with col1:
        reporter_name = st.text_input("Your Name *", placeholder="John Doe")
        location = st.text_input("Location *", placeholder="Street name, area, city")
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input("Latitude", value=26.9124, format="%.6f")
        with col_lon:
            longitude = st.number_input("Longitude", value=75.7873, format="%.6f")
        
        audio_text = st.text_area(
            "Additional Details (Audio Transcription)",
            placeholder="Describe the issue in detail...",
            height=100
        )
    
    with col2:
        uploaded_file = st.file_uploader(
            "Upload Image *",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the civic issue"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.markdown("---")
    
    if st.button("🚀 Submit Report", type="primary", use_container_width=True):
        if not reporter_name or not location or not uploaded_file:
            st.error("Please fill in all required fields (*)")
        else:
            with st.spinner("🔍 Analyzing image and detecting issues..."):
                files = {"image": uploaded_file.getvalue()}
                data = {
                    "reporter_name": reporter_name,
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "audio_text": audio_text or ""
                }
                
                try:
                    response = requests.post(
                        f"{API_URL}/api/report-issue",
                        files={"image": ("image.jpg", uploaded_file.getvalue(), "image/jpeg")},
                        data=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result["status"] == "no_issue":
                            st.info("ℹ️ No significant civic issue detected in the image.")
                            st.write(f"Confidence: {result['confidence']:.2%}")
                        else:
                            st.success("✅ Issue reported successfully!")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Issue ID", f"#{result['issue_id']}")
                            with col_b:
                                st.metric("Issue Type", result['issue_type'].replace("_", " ").title())
                            with col_c:
                                severity_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🚨"}
                                st.metric("Severity", f"{severity_emoji.get(result['severity'], '🔵')} {result['severity'].title()}")
                            
                            st.subheader("📋 Issue Description")
                            st.write(result['description'])
                            
                            st.subheader("💡 Suggested Actions")
                            actions = result['suggested_actions']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Immediate Actions:**")
                                for action in actions.get('immediate_actions', []):
                                    st.write(f"• {action}")
                                
                                st.markdown("**Citizen Actions:**")
                                for action in actions.get('citizen_actions', []):
                                    st.write(f"• {action}")
                            
                            with col2:
                                st.markdown("**Authority Actions:**")
                                for action in actions.get('authority_actions', []):
                                    st.write(f"• {action}")
                                
                                st.markdown("**Preventive Measures:**")
                                for action in actions.get('preventive_measures', []):
                                    st.write(f"• {action}")
                            
                            if result.get('agency_notified'):
                                st.success(f"🔔 Notification sent to: **{result['agency_notified']}**")
                            
                            st.balloons()
                    else:
                        st.error(f"Error: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API server. Please ensure the FastAPI server is running.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

with tab2:
    st.header("Recent Reports")
    
    try:
        response = requests.get(f"{API_URL}/api/issues")
        if response.status_code == 200:
            issues = response.json()["issues"]
            
            if not issues:
                st.info("No issues reported yet.")
            else:
                for issue in issues[:10]:  # Show latest 10
                    with st.expander(f"#{issue['id']} - {issue['issue_type'].replace('_', ' ').title()} | {issue['location']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Reporter:** {issue['reporter_name']}")
                            st.write(f"**Status:** {issue['status'].title()}")
                        with col2:
                            st.write(f"**Priority:** {issue['priority'].title()}")
                            st.write(f"**Agency:** {issue['assigned_agency'] or 'N/A'}")
                        with col3:
                            created = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                            st.write(f"**Reported:** {created.strftime('%Y-%m-%d %H:%M')}")
                        
                        st.write(f"**Description:** {issue['description']}")
    except:
        st.error("Failed to load reports. Please check API connection.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Powered by LangGraph • FastAPI • Groq • PostgreSQL • MCP</p>
</div>
""", unsafe_allow_html=True)