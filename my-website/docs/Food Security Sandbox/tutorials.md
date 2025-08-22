---
tags:
  - PADI
  - Digital Agriculture
---

# Tutorials

### Getting Started with the Food Security Sandbox

#### Prerequisites
- Docker and Docker Compose installed
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- MongoDB (or use the provided Docker container)

#### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Digital-Agriculture-Sandbox
   ```

2. **Config Environment**
   Create .env file in app-server with the following keys:
   - MONGODB_URI=mongodb://mongodb:27017/digital_agriculture
   - CLIENT_ID= your client id
   - CLIENT_KEY= your client key
   - TAPIS_BASE_URL=https://icicleai.tapis.io
   - TENANT=icicleai
   - APP_BASE_URL=http://localhost:3000
   - CALLBACK_URL=http://localhost:5003/api/oauth2/callback
     
   Create .env files in farmer-server and param-server with the following keys:
   - TAPIS_BASE_URL=https://icicleai.tapis.io
   - TENANT=icicleai

3. **Start the Application**
   ```bash
   docker compose -p digital-agriculture-sandbox up --build
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - App Server: http://localhost:5003
   - Farmer Server: http://localhost:5001
   - Param Server: http://localhost:5002

5. **Authentication**
   - Use TACC Tapis authentication
   - Register at https://accounts.tacc.utexas.edu/register
   - Use any other CILogon account such as Google, GitHub, ORCID
