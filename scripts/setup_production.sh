echo "🚀 Setting up Production Environment..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Install Nginx (for reverse proxy)
sudo apt-get install -y nginx

# Create application user
sudo useradd -m -s /bin/bash civicapp

# Setup application directory
sudo mkdir -p /opt/civic-issue-detection
sudo chown civicapp:civicapp /opt/civic-issue-detection

# Switch to app user
sudo -u civicapp bash << 'EOF'
cd /opt/civic-issue-detection

# Clone repository (replace with actual repo)
# git clone <repo-url> .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p uploads logs

# Setup environment
cp .env.example .env
echo "⚠️  Please edit /opt/civic-issue-detection/.env with your credentials"
EOF

# Setup PostgreSQL database
sudo -u postgres psql << EOF
CREATE DATABASE civic_issues;
CREATE USER civicapp WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE civic_issues TO civicapp;
EOF

# Setup systemd services
sudo tee /etc/systemd/system/civic-mcp.service > /dev/null << EOF
[Unit]
Description=Civic Issue Detection - MCP Server
After=network.target

[Service]
Type=simple
User=civicapp
WorkingDirectory=/opt/civic-issue-detection
Environment="PATH=/opt/civic-issue-detection/venv/bin"
ExecStart=/opt/civic-issue-detection/venv/bin/python mcp/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/civic-api.service > /dev/null << EOF
[Unit]
Description=Civic Issue Detection - FastAPI
After=network.target civic-mcp.service

[Service]
Type=simple
User=civicapp
WorkingDirectory=/opt/civic-issue-detection
Environment="PATH=/opt/civic-issue-detection/venv/bin"
ExecStart=/opt/civic-issue-detection/venv/bin/python api/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/civic-streamlit.service > /dev/null << EOF
[Unit]
Description=Civic Issue Detection - Streamlit
After=network.target civic-api.service

[Service]
Type=simple
User=civicapp
WorkingDirectory=/opt/civic-issue-detection
Environment="PATH=/opt/civic-issue-detection/venv/bin"
ExecStart=/opt/civic-issue-detection/venv/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target