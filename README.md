# 🚀 JamfTerraform

AI-powered Terraform HCL generator for Jamf Pro configurations. Generate infrastructure-as-code from natural language using Google Gemini AI.

## 📋 Overview

JamfTerraform is a comprehensive toolset for managing Jamf Pro configurations using Terraform. It consists of three main components:

1. **Backend** - FastAPI service with Gemini AI integration
2. **Frontend** - React web application with modern UI
3. **Agent** - Tauri desktop application for local execution (coming soon)

## ✨ Features

### Current

- 🤖 **AI-Powered Generation**: Convert natural language to Terraform HCL
- 💬 **Chat Interface**: Interactive conversation for iterative configuration
- 📦 **Proporter Export**: Export entire Jamf Pro instances as Terraform code (6.7x faster with optimizations)
- 🎨 **Premium UI**: Modern dark theme with smooth animations
- 🔒 **Secure**: Environment-based API key management
- 📊 **Health Monitoring**: Real-time backend status

### Coming Soon

- 🖥️ **Local Execution**: Run Terraform via desktop agent
- ☁️ **Cloud Execution**: Managed execution environment
- 📝 **Configuration Templates**: Pre-built Jamf configurations
- 🔄 **State Management**: Terraform state tracking

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │ ← React + TypeScript
│  (Port 5173)    │
└────────┬────────┘
         │
         │ HTTP
         ▼
┌─────────────────┐
│    Backend      │ ← FastAPI + Python
│  (Port 8000)    │
└────────┬────────┘
         │
         │ API
         ▼
┌─────────────────┐
│  Gemini API     │ ← Google AI
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- Google Gemini API key

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Access Application

Open your browser to `http://localhost:5173`

## 📁 Project Structure

```
JamfTerraform/
├── backend/              # FastAPI backend
│   ├── main.py          # API routes
│   ├── llm_service.py   # Gemini integration
│   ├── models.py        # Pydantic models
│   ├── config.py        # Configuration
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── services/    # API services
│   │   ├── types/       # TypeScript types
│   │   └── App.tsx      # Main app
│   └── package.json
└── agent/               # Tauri agent (coming soon)
```

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

### Frontend Configuration

The frontend connects to the production backend by default.

- **Production**: `https://jamfterraform-production.up.railway.app`
- **Local Development**: Change `API_BASE_URL` in `src/services/ExecutionService.ts` to `http://localhost:8000`

## 📖 Usage

### Generate HCL via Chat

1. Navigate to the **Chat & Generate** tab
2. Describe your Jamf configuration in natural language
3. The AI will generate the corresponding Terraform HCL
4. Copy and use the generated code

Example prompts:

- "Create a Jamf policy to install Google Chrome on all computers"
- "Generate a configuration profile for Wi-Fi settings"
- "Create a smart group for MacBooks running macOS 14+"

### Export Jamf Instance with Proporter

1. Navigate to the **Proporter** tab
2. Enter your Jamf Pro credentials
3. Click **"Generate Instance Summary"** to scan your Jamf Pro server
4. Review the resources found (policies, scripts, profiles, groups, etc.)
5. Click **"Export Entire Instance"** to download everything as a ZIP file

The export includes:

- Terraform HCL for all resources
- Support files (scripts, configuration profile payloads)
- Provider configuration
- Validation report
- README with usage instructions

**Performance**: Exports ~460 resources in ~45 seconds with 6.7x speedup from parallel processing.

## 🎨 Design Philosophy

- **Security First**: API keys never logged or committed
- **User Experience**: Premium, responsive UI with smooth interactions
- **Type Safety**: Full TypeScript coverage
- **Code Quality**: PEP 8 for Python, ESLint for TypeScript
- **Pure HCL Output**: No markdown or explanatory text in generated code

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Run tests
python test_api.py
```

### Frontend Development

```bash
cd frontend
npm run dev

# Build for production
npm run build

# Lint
npm run lint
```

## 📝 API Documentation

### Backend Endpoints

#### `GET /healthz`

Health check endpoint.

**Response**: `{"status": 200}`

#### `POST /api/generate`

Generate HCL from prompt.

**Request**:

```json
{
  "prompt": "Create a Jamf policy",
  "context": "optional existing config"
}
```

**Response**:

```json
{
  "hcl": "resource \"jamfpro_policy\" ...",
  "success": true,
  "error": null
}
```

## 🔒 Security

- ✅ API keys stored in environment variables only
- ✅ `.gitignore` prevents accidental commits
- ✅ CORS restricted to specific origins
- ✅ No sensitive data in HCL output
- ✅ Input validation with Pydantic

## 🛡️ Validation & Safety

The backend now includes a strict **Intent Validator** to ensure generated configurations are safe and accurate:

- **Safe Scoping**: "All Computers" targeting is blocked by default to prevent accidental mass-deployments. You must target specific groups or IDs.
- **App Catalog Accuracy**: App Installer names are validated against the official Jamf App Catalog. Fuzzy matching suggests corrections for typos (e.g. "Google Chrm" -> "Google Chrome").
- **Script Safety**: Scripts are scanned for empty content and common dangerous commands (e.g. `rm -rf /`).

## 🤝 Contributing

This is a workspace project. Follow the workspace rules:

1. **Security First**: Never commit API keys
2. **Code Style**: PEP 8 for Python, TypeScript for React
3. **HCL Output**: Pure HCL only, no markdown
4. **Portability**: Use ExecutionService for all API calls

## 📄 License

This project is for internal use.

## 🙏 Acknowledgments

- **Terraform**: Infrastructure as Code
- **Jamf Pro**: Apple device management
- **Google Gemini**: AI-powered generation
- **FastAPI**: Modern Python web framework
- **React**: UI library
- **Vite**: Build tool
