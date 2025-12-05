from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import (GenerateHCLRequest, GenerateHCLResponse, JamfResourcesRequest, 
                   JamfResourceListResponse, JamfInstanceExportRequest, JamfInstanceExportResponse,
                   JamfInstanceSummary, JamfResourceDetailRequest, JamfResourceDetailResponse, 
                   ResourceDependency, BulkExportRequest)
from llm_service import get_llm_service
from jamf_client import JamfClient
from dependency_resolver import DependencyResolver
from hcl_generator import HCLGenerator
from recursive_fetcher import RecursiveFetcher
from collections import defaultdict
import json
import zipfile
import io
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
        
        # Fetch detailed resource data recursively
        fetcher = RecursiveFetcher(client)
        all_resources = await fetcher.fetch_all(request.resource_type, request.resource_id)
        
        # Find root resource data
        resource_data = next((d for t, d in all_resources if t == request.resource_type and d.get('id') == request.resource_id), None)
        
        if not resource_data:
             # Fallback: resource might be found but ID mismatch type?
             # Try simple fetch if recursive failed to identify root?
             # Or raise error.
             raise ValueError(f"Root resource data not found for {request.resource_type} {request.resource_id}")

        # Extract dependencies (direct only, for UI tree)
        resolver = DependencyResolver()
        deps_dict = resolver.extract_dependencies(request.resource_type, resource_data)
        
        # Convert to ResourceDependency models
        dependencies = []
        for dep_type, dep_ids in deps_dict.items():
            for dep_id in dep_ids:
                dependencies.append(ResourceDependency(
                    type=dep_type,
                    id=dep_id,
                    name=f"{dep_type}_{dep_id}"
                ))
        
        # Generate HCL
        hcl_generator = HCLGenerator()
        hcl = hcl_generator.generate_resource_hcl(request.resource_type, resource_data)
        
        # Generate Bundle HCL (Dependencies included)
        resources_by_type = defaultdict(list)
        for r_type, r_data in all_resources:
            resources_by_type[r_type].append(r_data)
            
        sorted_resources = resolver.topological_sort(resources_by_type)
        bundle_hcl = hcl_generator.generate_file(sorted_resources)
        
        return JamfResourceDetailResponse(
            resource=resource_data,
            dependencies=dependencies,
            hcl=hcl,
            bundle_hcl=bundle_hcl,
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
            dependencies=[],
            success=False,
            error=f"Failed to fetch resource details: {str(e)}"
        )


@app.post("/api/jamf/bulk-export")
async def bulk_export_resources(request: BulkExportRequest):
    """
    Export multiple resources and their dependencies as a ZIP file.
    """
    try:
        client = JamfClient(
            request.credentials.url,
            request.credentials.username,
            request.credentials.password
        )
        await client.get_auth_token()
        
        fetcher = RecursiveFetcher(client)
        resolver = DependencyResolver()
        hcl_gen = HCLGenerator()
        
        # Deduplication cache: (type, id) -> data
        all_unique_resources = {}

        # 1. Fetch all requested resources + dependencies
        for res in request.resources:
            try:
                fetched = await fetcher.fetch_all(res.type, res.id, recursive=request.include_dependencies)
                for r_type, r_data in fetched:
                    r_id = r_data.get('id')
                    if r_id is None:
                        # Try general.id which is common in Jamf objects (Policy, Profile, etc.)
                        r_id = r_data.get('general', {}).get('id')
                    
                    if r_id is not None:
                        key = (r_type, str(r_id))
                        all_unique_resources[key] = (r_type, r_data)
            except Exception as e:
                print(f"Error fetching {res.type} {res.id} for bulk export: {e}")
                continue

        # 2. Prepare for sorting
        resources_by_type = defaultdict(list)
        for (r_type, _), (orig_type, r_data) in all_unique_resources.items():
            resources_by_type[orig_type].append(r_data)

        # 3. Topological Sort
        sorted_tuples = resolver.topological_sort(resources_by_type)
        
        # 4. Organize content by file type
        files_content = defaultdict(list)
        
        for r_type, r_data in sorted_tuples:
            chunk = hcl_gen.generate_resource_hcl(r_type, r_data)
            filename = f"{r_type}.tf"
            files_content[filename].append(chunk)

        # 5. Create ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Write resource files
            for filename, blocks in files_content.items():
                content = "\\n\\n".join(blocks)
                zip_file.writestr(filename, content)
            
            # Write provider configuration
            provider_hcl = f"""
terraform {{
  required_providers {{
    jamfpro = {{
      source = "jamf/jamfpro"
      version = "~> 0.4.0"
    }}
  }}
}}

provider "jamfpro" {{
  instance_url = "{request.credentials.url}"
}}
"""
            zip_file.writestr("provider.tf", provider_hcl)
            
            readme = """# Jamf Pro Terraform Export
Generated by JamfTerraform Proporter.
1. Configure auth in provider.tf
2. terraform init
3. terraform plan
"""
            zip_file.writestr("README.md", readme)

        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer, 
            media_type="application/zip", 
            headers={"Content-Disposition": "attachment; filename=jamf_export.zip"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
