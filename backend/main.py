from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (GenerateHCLRequest, GenerateHCLResponse, JamfResourcesRequest, 
                   JamfResourceListResponse, JamfInstanceExportRequest, JamfInstanceExportResponse,
                   JamfInstanceSummary, JamfResourceDetailRequest, JamfResourceDetailResponse, 
                   ResourceDependency)
from llm_service import get_llm_service
from jamf_client import JamfClient
from dependency_resolver import DependencyResolver
from hcl_generator import HCLGenerator
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
        "https://jamfaform.workshopse.com",  # Custom Domain
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


@app.post("/api/jamf/resources", response_model=JamfResourceListResponse)
async def list_jamf_resources(request: JamfResourcesRequest):
    """
    List resources from a Jamf Pro instance.
    
    Args:
        request: JamfResourcesRequest with credentials and resource type
        
    Returns:
        JamfResourceListResponse with list of resources
    """
    try:
        client = JamfClient(
            url=request.credentials.url,
            username=request.credentials.username,
            password=request.credentials.password
        )
        
        resources = await client.get_resources(request.resource_type)
        
        return JamfResourceListResponse(
            resources=resources,
            resource_type=request.resource_type,
            success=True,
            error=None
        )
    except ValueError as e:
        return JamfResourceListResponse(
            resources=[],
            resource_type=request.resource_type,
            success=False,
            error=str(e)
        )
    except Exception as e:
        return JamfResourceListResponse(
            resources=[],
            resource_type=request.resource_type,
            success=False,
            error=f"Failed to fetch resources: {str(e)}"
        )


@app.post("/api/jamf/instance-export", response_model=JamfInstanceExportResponse)
async def export_jamf_instance(request: JamfInstanceExportRequest):
    """
    Export all or selected resources from a Jamf Pro instance as HCL.
    
    Args:
        request: JamfInstanceExportRequest with credentials and optional selected types
        
    Returns:
        JamfInstanceExportResponse with HCL and resource summary
    """
    try:
        client = JamfClient(
            url=request.credentials.url,
            username=request.credentials.username,
            password=request.credentials.password
        )
        
        # Fetch all resources (summary only for now - just id/name)
        all_resources = await client.get_all_instance_resources()
        
        # Build summary
        summary = []
        for res_type, items in all_resources.items():
            summary.append(JamfInstanceSummary(
                resource_type=res_type,
                count=len(items),
                items=items
            ))
        
        # For Phase 3, we'll generate HCL
        # For now, return placeholder
        hcl_generator = HCLGenerator()
        dependency_resolver = DependencyResolver()
        
        # Note: Full implementation would fetch detailed data for each resource
        # and resolve dependencies. For MVP, generate simple placeholder HCL
        hcl = "# Jamf Pro Instance Export\n"
        hcl += "# This is a Phase 3 MVP - full HCL generation coming soon\n\n"
        
        for res_type, items in all_resources.items():
            hcl += f"# {res_type.upper()}: {len(items)} resources\n"
        
        return JamfInstanceExportResponse(
            summary=summary,
            hcl=hcl,
            success=True,
            error=None
        )
    except ValueError as e:
        return JamfInstanceExportResponse(
            summary=[],
            hcl="",
            success=False,
            error=str(e)
        )
    except Exception as e:
        return JamfInstanceExportResponse(
            summary=[],
            hcl="",
            success=False,
            error=f"Failed to export instance: {str(e)}"
        )


@app.post("/api/jamf/resource-detail", response_model=JamfResourceDetailResponse)
async def get_resource_detail(request: JamfResourceDetailRequest):
    """
    Get detailed information about a specific resource including dependencies and HCL.
    
    Args:
        request: JamfResourceDetailRequest with credentials, resource type, and ID
        
    Returns:
        JamfResourceDetailResponse with full resource data, dependencies, and HCL
    """
    try:
        client = JamfClient(
            url=request.credentials.url,
            username=request.credentials.username,
            password=request.credentials.password
        )
        
        await client.get_auth_token()
        
        # Fetch detailed resource data
        resource_data = {}
        if request.resource_type == "policies":
            resource_data = await client.get_policy_detail(request.resource_id)
        elif request.resource_type == "scripts":
            resource_data = await client.get_script_detail(request.resource_id)
        elif request.resource_type == "packages":
            resource_data = await client.get_package_detail(request.resource_id)
        elif request.resource_type == "config-profiles":
            resource_data = await client.get_configuration_profile_detail(request.resource_id)
        elif request.resource_type == "smart-groups":
            resource_data = await client.get_computer_group_detail(request.resource_id)
        elif request.resource_type == "jamf-app-catalog":
            resource_data = await client.get_jamf_app_catalog_detail(request.resource_id)
        # Add more resource types as needed
        else:
            return JamfResourceDetailResponse(
                resource={},
                hcl="",
                success=False,
                error=f"Resource type {request.resource_type} not supported yet"
            )
        
        # Extract dependencies
        resolver = DependencyResolver()
        deps_dict = resolver.extract_dependencies(request.resource_type, resource_data)
        
        # Convert to ResourceDependency models
        dependencies = []
        for dep_type, dep_ids in deps_dict.items():
            for dep_id in dep_ids:
                # For now, use ID as name (could fetch actual names if needed)
                dependencies.append(ResourceDependency(
                    type=dep_type,
                    id=dep_id,
                    name=f"{dep_type}_{dep_id}"
                ))
        
        # Generate HCL
        hcl_generator = HCLGenerator()
        hcl = hcl_generator.generate_resource_hcl(request.resource_type, resource_data)
        
        return JamfResourceDetailResponse(
            resource=resource_data,
            dependencies=dependencies,
            hcl=hcl,
            success=True
        )
        
    except ValueError as e:
        return JamfResourceDetailResponse(
            resource={},
            hcl="",
            success=False,
            error=str(e)
        )
    except Exception as e:
        return JamfResourceDetailResponse(
            resource={},
            hcl="",
            success=False,
            error=f"Failed to fetch resource details: {str(e)}"
        )
