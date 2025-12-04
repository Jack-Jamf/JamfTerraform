# JamfTerraform Backend

FastAPI backend service for generating Terraform HCL configurations using Google Gemini AI.

## Features

- **LLM Integration**: Uses Google Gemini API to generate HCL configurations
- **HCL Generation**: Converts natural language prompts into Terraform HCL for Jamf Pro
- **Security**: Environment-based API key management (never logs or commits tokens)
- **CORS Support**: Configured for frontend and agent communication

## Setup

1. **Install dependencies**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the server**:
   ```bash
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

## API Endpoints

### `GET /healthz`

Health check endpoint.

**Response**:

```json
{ "status": 200 }
```

### `POST /api/generate`

Generate HCL configuration from a natural language prompt.

**Request**:

```json
{
  "prompt": "Create a Jamf policy to install Chrome",
  "context": "optional existing configuration"
}
```

**Response**:

```json
{
  "hcl": "resource \"jamfpro_policy\" \"install_chrome\" {...}",
  "success": true,
  "error": null
}
```

## Project Structure

```
backend/
├── main.py           # FastAPI application and routes
├── llm_service.py    # Gemini API integration
├── models.py         # Pydantic request/response models
├── config.py         # Configuration and system prompt
├── requirements.txt  # Python dependencies
├── .env.example      # Environment template
└── .gitignore        # Git ignore rules
```

## Security Notes

- API keys are loaded from environment variables only
- Never commit `.env` file to version control
- The system prompt enforces no sensitive data in HCL output
- CORS is configured for specific origins only
