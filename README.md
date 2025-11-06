# 🏙️ Multi-Agent Civic Issue Detection System

A production-ready AI-powered system for detecting and reporting civic issues using multi-agent architecture.

## 🚀 Features

- **Multi-Agent Architecture**: Powered by LangGraph with specialized agents
  - Issue Detector Agent (Vision AI)
  - Action Planner Agent
  - Notification Agent
  - Orchestrator for workflow management

- **Technologies**
  - 🤖 **LangGraph**: Multi-agent workflow orchestration
  - ⚡ **FastAPI**: High-performance API backend
  - 🔌 **MCP**: Model Context Protocol for AI context management
  - 🐘 **PostgreSQL**: Robust data persistence
  - 🎨 **Streamlit**: Interactive web interface
  - 🧠 **Groq**: Ultra-fast AI inference (Llama 3.2 Vision + Llama 3.3)

- **Capabilities**
  - Detect water leaks and wastage
  - Identify unpicked garbage and litter
  - Spot potholes and road damage
  - Recognize criminal/violent activities
  - Automatic agency routing
  - Smart action suggestions
  - Real-time notifications

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Groq API Key ([Get it here](https://console.groq.com))
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd civic-issue-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. **Setup PostgreSQL**
```bash
# Create database
createdb civic_issues

# Or using psql
psql -U postgres
CREATE DATABASE civic_issues;
\q
```

6. **Initialize database**
```bash
python database/seed_data.py
```

7. **Start services**
```bash
chmod +x run_services.sh
./run_services.sh
```

### Docker Setup

```bash
# Create .env file with GROQ_API_KEY
echo "GROQ_API_KEY=your_key_here" > .env

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec api python database/seed_data.py

# View logs
docker-compose logs -f
```

## 🎯 Usage

### Access Points

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **MCP Server**: http://localhost:8001

### API Endpoints

#### Report Issue
```bash
curl -X POST "http://localhost:8000/api/report-issue" \
  -F "image=@photo.jpg" \
  -F "reporter_name=John Doe" \
  -F "location=MG Road, Jaipur" \
  -F "latitude=26.9124" \
  -F "longitude=75.7873" \
  -F "audio_text=Water pipe burst near the main road"
```

#### Get All Issues
```bash
curl "http://localhost:8000/api/issues"
```

#### Get Specific Issue
```bash
curl "http://localhost:8000/api/issues/1"
```

### Web Interface

1. Open http://localhost:8501
2. Fill in your details
3. Upload an image of the civic issue
4. Add any additional context
5. Click "Submit Report"
6. View AI analysis and suggested actions
7. Agency notification sent automatically

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│                  (User Interface Layer)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                   (API & Business Logic)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
┌─────────────────┐  ┌──────────────┐  ┌─────────────┐
│   PostgreSQL    │  │ MCP Server   │  │  LangGraph  │
│   (Database)    │  │  (Context)   │  │ (Workflow)  │
└─────────────────┘  └──────────────┘  └─────────────┘
                                               │
                              ┌────────────────┼────────────────┐
                              │                │                │
                              ▼                ▼                ▼
                     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                     │   Detector   │ │   Planner    │ │  Notifier    │
                     │    Agent     │ │    Agent     │ │    Agent     │
                     └──────────────┘ └──────────────┘ └──────────────┘
                              │                │                │
                              └────────────────┼────────────────┘
                                              ▼
                                    ┌──────────────────┐
                                    │   Groq AI API    │
                                    │ (Vision + LLM)   │
                                    └──────────────────┘
```

## 🔄 Workflow

1. **Input Reception**: User submits image + details via Streamlit
2. **Issue Detection**: Vision AI (Llama 3.2 90B Vision) analyzes image
3. **Action Planning**: LLM generates contextual action suggestions
4. **Agency Routing**: System routes to appropriate department
5. **Notification**: Professional alert sent to agency
6. **Database Storage**: All data persisted in PostgreSQL
7. **User Feedback**: Real-time updates and action items

## 📊 Database Schema

### civic_issues
- id, reporter_name, location, latitude, longitude
- issue_type, description, severity, priority
- image_path, audio_path, status
- assigned_agency, suggested_actions
- created_at, updated_at

### agencies
- id, name, department, email, phone
- issue_types (JSON array)

### notifications
- id, issue_id, agency_id, message
- status, created_at

## 🔧 Configuration

### Environment Variables

```env
GROQ_API_KEY=gsk_...                    # Required: Your Groq API key
DATABASE_URL=postgresql://...            # PostgreSQL connection string
MCP_SERVER_URL=http://localhost:8001    # MCP server endpoint
FASTAPI_PORT=8000                       # API server port
STREAMLIT_PORT=8501                     # Streamlit port
```

### Groq Models Used

- **Vision**: `meta-llama/llama-4-maverick-17b-128e-instruct` (Issue detection)
- **Text**: `llama-3.3-70b-versatile` (Action planning & notifications)

## 🧪 Testing

```bash
# Test MCP Server
curl http://localhost:8001/mcp/health

# Test FastAPI
curl http://localhost:8000/api/issues

# Run with sample data
python -c "
import requests
response = requests.post('http://localhost:8000/api/report-issue',
    files={'image': open('test_image.jpg', 'rb')},
    data={'reporter_name': 'Test User', 'location': 'Test Location'})
print(response.json())
"
```

## 📱 Production Deployment

### Scaling Considerations

1. **Database**: Use managed PostgreSQL (AWS RDS, Azure Database)
2. **API**: Deploy behind load balancer (multiple FastAPI instances)
3. **File Storage**: Use S3/Azure Blob for images
4. **Caching**: Add Redis for frequent queries
5. **Monitoring**: Integrate Sentry, DataDog, or Prometheus

### Security

- Enable HTTPS/TLS
- Add authentication (JWT tokens)
- Rate limiting on API endpoints
- Input validation and sanitization
- SQL injection protection (SQLAlchemy ORM)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Groq for ultra-fast AI inference
- Anthropic for LangGraph framework
- FastAPI team for excellent web framework
- Streamlit for rapid UI development

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check documentation at `/docs`
- Contact: support@civic-ai.example.com

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] SMS/Email integration
- [ ] Geospatial clustering
- [ ] Historical trend analysis
- [ ] Citizen feedback loop
- [ ] API rate limiting
- [ ] Automated testing suite

---

Built with ❤️ using AI Multi-Agent Architecture