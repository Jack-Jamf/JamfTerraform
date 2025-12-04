# JamfTerraform User Guide

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Terraform installed
- Google Gemini API key
- Jamf Pro API token

### Starting the Application

**Terminal 1 - Backend**:

```bash
cd backend
source venv/bin/activate
uvicorn main:app --port 8000
```

**Terminal 2 - Frontend**:

```bash
cd frontend
npm run dev
```

**Terminal 3 - Agent** (optional):

```bash
cd agent
npm run tauri dev
```

## Using the Web Application

### 1. Generate HCL from Recipes

1. Open http://localhost:5173
2. Click the **Recipe Cookbook** tab
3. Browse the 6 pre-built templates:
   - Install Google Chrome
   - macOS Version Smart Group
   - Wi-Fi Configuration
   - Software Update Policy
   - MacBook Smart Group
   - Security Settings
4. Click any recipe card
5. The chat tab opens with the recipe prompt pre-filled
6. Click **Send** to generate HCL
7. Copy the generated code

### 2. Generate HCL from Natural Language

1. Open http://localhost:5173
2. Stay on the **Chat & Generate** tab
3. Type your request in natural language:
   - "Create a policy to install Slack"
   - "Make a smart group for computers with less than 10GB free space"
   - "Create a configuration profile for screen saver settings"
4. Click **Send** or press Enter
5. View the syntax-highlighted HCL output
6. Copy the generated code

## Using the Tauri Agent

### Execute Terraform Locally

1. **Open the Agent** (should already be running from `npm run tauri dev`)
2. **Paste HCL Code**:
   - Copy HCL from the web app
   - Paste into the "HCL Code" textarea
   - Preview shows syntax-highlighted code
3. **Enter Jamf Token**:
   - Paste your Jamf Pro API token
   - Token is masked (password field)
4. **Execute**:
   - Click **▶️ Execute Terraform**
   - Watch real-time output
   - Green text = stdout
   - Red text = stderr
5. **Clear Output** (optional):
   - Click **🗑️ Clear Output** to reset

## Example Workflows

### Workflow 1: Deploy Software

1. **Web App**: "Create a policy to install Microsoft Office"
2. **Copy** the generated HCL
3. **Agent**: Paste HCL + add token
4. **Execute**: Watch Terraform create the policy
5. **Verify**: Check Jamf Pro for the new policy

### Workflow 2: Create Smart Group

1. **Web App**: Click "macOS Version Smart Group" recipe
2. **Generate**: Click Send
3. **Copy** the HCL
4. **Agent**: Paste + execute
5. **Verify**: Smart group appears in Jamf Pro

### Workflow 3: Configuration Profile

1. **Web App**: "Create a configuration profile for FileVault"
2. **Generate** and copy HCL
3. **Agent**: Execute with token
4. **Verify**: Profile created in Jamf Pro

## Tips & Best Practices

### For Best Results

**When using Chat**:

- Be specific about what you want
- Mention resource types (policy, smart group, config profile)
- Include relevant details (targeting, frequency, settings)

**Example Good Prompts**:

- ✅ "Create a Jamf policy to install Google Chrome on all computers, running once per computer"
- ✅ "Make a smart group for MacBook Pros running macOS 14 or higher"
- ✅ "Create a configuration profile to set the screen saver timeout to 10 minutes"

**Example Vague Prompts**:

- ❌ "Install Chrome"
- ❌ "Make a group"
- ❌ "Set screen saver"

### Security

**API Keys**:

- Backend API key stored in `.env` (never committed)
- Agent token passed as environment variable
- Tokens never appear in logs

**Temporary Files**:

- Agent creates temp directory for each execution
- Automatically cleaned up after completion
- No file system pollution

## Troubleshooting

### Backend Issues

**"Backend Offline" in web app**:

```bash
# Check if backend is running
curl http://localhost:8000/healthz

# Restart backend
cd backend
source venv/bin/activate
uvicorn main:app --port 8000
```

**"GEMINI_API_KEY not set"**:

```bash
cd backend
cp .env.example .env
# Edit .env and add your API key
```

### Frontend Issues

**Web app not loading**:

```bash
# Check if frontend is running
curl http://localhost:5173

# Restart frontend
cd frontend
npm run dev
```

**"Failed to fetch cookbook"**:

- Ensure backend is running
- Check browser console for errors

### Agent Issues

**Agent won't start**:

```bash
# Check Rust installation
rustc --version

# Rebuild agent
cd agent/src-tauri
cargo build
```

**"Failed to spawn terraform"**:

- Ensure Terraform is installed: `terraform --version`
- Add Terraform to PATH

**No output streaming**:

- Check browser console for event listener errors
- Verify Tauri event system is working

## API Reference

### Backend Endpoints

**GET /healthz**

- Health check
- Returns: `{"status": 200}`

**POST /api/generate**

- Generate HCL from prompt
- Request:
  ```json
  {
    "prompt": "Create a Jamf policy",
    "context": "optional"
  }
  ```
- Response:
  ```json
  {
    "hcl": "resource \"jamfpro_policy\" ...",
    "success": true,
    "error": null
  }
  ```

**GET /api/cookbook**

- Get recipe templates
- Returns: Array of 6 modules

### Agent Commands

**run_terraform**

- Execute Terraform with HCL
- Parameters:
  - `hclCode`: String (HCL configuration)
  - `jamfToken`: String (Jamf API token)
- Events: `terraform-output` (real-time streaming)
- Returns: Success/error message

## Advanced Usage

### Custom Recipes

Edit `backend/cookbook_modules.json` to add your own recipes:

```json
{
  "id": "custom-recipe",
  "title": "My Custom Recipe",
  "description": "Description here",
  "category": "Policies",
  "icon": "🎯",
  "tags": ["custom"],
  "prompt": "Your prompt here"
}
```

### Environment Variables

**Backend** (`.env`):

```
GEMINI_API_KEY=your_key_here
```

**Agent** (runtime):

- `JAMF_TOKEN`: Passed automatically to Terraform

## Support

### Logs

**Backend logs**: Terminal running uvicorn
**Frontend logs**: Browser console (F12)
**Agent logs**: Tauri dev console

### Testing

Run end-to-end tests:

```bash
./test-e2e.sh
```

## What's Next?

Potential enhancements:

- Terraform plan (dry-run)
- Execution history
- Save/load HCL files
- Multi-file projects
- Terraform state management
