from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GenerateHCLRequest, GenerateHCLResponse
from llm_service import get_llm_service
import json
from pathlib import Path

app = FastAPI(title="JamfTerraform Backend", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local frontend dev
        "http://localhost:1420",  # Tauri agent
        "https://jamfaform-production.up.railway.app",  # Railway backend (for testing)
        "*"  # Allow all origins (you can restrict this later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    """Health check endpoint."""
    return {"status": 200}


@app.post("/api/generate", response_model=GenerateHCLResponse)
async def generate_hcl(request: GenerateHCLRequest):
    """
    Generate HCL configuration from user prompt with scope confirmation.
    
    Args:
        request: GenerateHCLRequest with prompt, optional context, and scope_confirmation
        
    Returns:
        GenerateHCLResponse with generated HCL, confirmation request, or error
    """
    try:
        # Check if this is a policy-related request
        is_policy_request = any(keyword in request.prompt.lower() for keyword in [
            'policy', 'install', 'deploy', 'configure', 'update', 'script', 'package'
        ])
        
        # If it's a policy request and no scope confirmation yet, ask for it
        if is_policy_request and request.scope_confirmation is None:
            return GenerateHCLResponse(
                hcl="",
                success=True,
                requires_confirmation=True,
                confirmation_message=(
                    "Before I generate this policy, I need to know the scope:\n\n"
                    "**How should this policy be targeted?**\n\n"
                    "1. **Specific group** - Reply with the group name (e.g., 'IT Department', 'Sales Team')\n"
                    "2. **All computers** - Reply 'all computers' (⚠️ will affect all devices)\n"
                    "3. **Custom** - Specify department, building, or computer IDs\n\n"
                    "💡 **Tip**: For safety, I recommend targeting a specific group first."
                )
            )
        
        # If we have scope confirmation, add it to the context
        context = request.context or ""
        if request.scope_confirmation:
            scope_lower = request.scope_confirmation.lower()
            
            if 'all computer' in scope_lower:
                context += f"\n\nSCOPE INSTRUCTION: User confirmed they want to target ALL COMPUTERS. Use computer_group_ids = [1] with comment '# Replace with All Computers group ID'."
            else:
                # User specified a group/department/etc
                context += f"\n\nSCOPE INSTRUCTION: User wants to target: {request.scope_confirmation}. Use appropriate targeting (computer_group_ids, department_ids, etc.) with placeholder ID and comment to replace with actual ID."
        
        # Generate HCL
        llm_service = get_llm_service()
        hcl = llm_service.generate_hcl(request.prompt, context)
        
        return GenerateHCLResponse(
            hcl=hcl,
            success=True,
            error=None,
            requires_confirmation=False
        )
    except ValueError as e:
        # Configuration error (e.g., missing API key)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # API or other errors
        return GenerateHCLResponse(
            hcl="",
            success=False,
            error=f"Failed to generate HCL: {str(e)}"
        )


@app.get("/api/cookbook")
async def get_cookbook():
    """
    Get cookbook modules/recipes.
    
    Returns:
        JSON object with cookbook modules
    """
    cookbook_path = Path(__file__).parent / "cookbook_modules.json"
    
    if not cookbook_path.exists():
        raise HTTPException(status_code=404, detail="Cookbook file not found")
    
    with open(cookbook_path, 'r') as f:
        cookbook_data = json.load(f)
    
    return cookbook_data

