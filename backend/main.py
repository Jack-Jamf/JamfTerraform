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
    allow_origins=["http://localhost:5173", "http://localhost:1420"],  # Frontend and agent
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
    Generate HCL configuration from user prompt.
    
    Args:
        request: GenerateHCLRequest with prompt and optional context
        
    Returns:
        GenerateHCLResponse with generated HCL or error
    """
    try:
        llm_service = get_llm_service()
        hcl = llm_service.generate_hcl(request.prompt, request.context)
        
        return GenerateHCLResponse(
            hcl=hcl,
            success=True,
            error=None
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

