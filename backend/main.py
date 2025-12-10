from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import (GenerateHCLRequest, GenerateHCLResponse, JamfResourcesRequest, 
                   JamfResourceListResponse, JamfInstanceExportRequest, JamfInstanceExportResponse,
    JamfInstanceSummary, JamfResourceDetailRequest, JamfResourceDetailResponse, 
    ResourceDependency, BulkExportRequest, JamfAuthRequest, JamfAuthResponse)
from llm_service import get_llm_service
from jamf_client import JamfClient
from dependency_resolver import DependencyResolver
from hcl_generator import HCLGenerator, PROVIDER_VERSION
from recursive_fetcher import RecursiveFetcher
from support_file_handler import SupportFileHandler
from export_validator import ExportValidator, generate_validation_report
from collections import defaultdict
import asyncio
import json
import zipfile
import io
from pathlib import Path
from datetime import datetime



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
    expose_headers=["Content-Type", "Content-Disposition", "Content-Length"]  # Expose headers to JavaScript
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


@app.post("/api/jamf/verify-auth", response_model=JamfAuthResponse)
async def verify_auth_credentials(request: JamfAuthRequest):
    """
    Verify Jamf Pro credentials by attempting to get an auth token.
    
    Args:
        request: JamfAuthRequest with credentials
        
    Returns:
        JamfAuthResponse with success status
    """
    try:
        client = JamfClient(
            url=request.credentials.url,
            username=request.credentials.username,
            password=request.credentials.password
        )
        
        token = await client.get_auth_token()
        
        return JamfAuthResponse(
            success=True,
            token=token,
            error=None
        )
    except ValueError as e:
        # Auth failure usually raises ValueError from JamfClient
        return JamfAuthResponse(
            success=False,
            token=None,
            error=str(e)
        )
    except Exception as e:
        return JamfAuthResponse(
            success=False,
            token=None,
            error=f"Connection failed: {str(e)}"
        )


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
    
    Includes support files (scripts, config profile payloads) as separate files
    in a support_files/ directory, referenced via Terraform's file() function.
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
        
        # Initialize support file handler for downloading scripts and profiles
        support_handler = SupportFileHandler(client)
        
        # HCL generator with support file handler for file() references
        hcl_gen = HCLGenerator(support_file_handler=support_handler)
        
        # Deduplication cache: (type, id) -> data
        all_unique_resources = {}

        # 1. Fetch all requested resources + dependencies IN PARALLEL (with rate limiting)
        print(f"[BULK EXPORT] Received {len(request.resources)} resources to export")
        
        # Limit concurrent requests to avoid overwhelming Jamf API (prevents 503 errors)
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
        
        async def fetch_single_resource(idx, res):
            """Helper to fetch a single resource with error handling and rate limiting."""
            async with semaphore:  # Limit concurrency
                print(f"[BULK EXPORT] Processing {idx+1}/{len(request.resources)}: {res.type} ID {res.id}")
                try:
                    fetched = await fetcher.fetch_all(res.type, res.id, recursive=request.include_dependencies)
                    print(f"[BULK EXPORT] Fetched {len(fetched)} items for {res.type} {res.id}")
                    return fetched
                except Exception as e:
                    print(f"Error fetching {res.type} {res.id} for bulk export: {e}")
                    return []
        
        # Fetch all resources in parallel (OPTIMIZATION: 5-10x speedup, rate-limited)
        fetch_tasks = [fetch_single_resource(idx, res) for idx, res in enumerate(request.resources)]
        all_fetched_results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        
        # Deduplicate and collect all resources
        for fetched_list in all_fetched_results:
            if isinstance(fetched_list, Exception):
                print(f"Fetch task failed with exception: {fetched_list}")
                continue
            
            for r_type, r_data in fetched_list:
                r_id = r_data.get('id')
                if r_id is None:
                    # Try general.id which is common in Jamf objects (Policy, Profile, etc.)
                    r_id = r_data.get('general', {}).get('id')
                
                if r_id is not None:
                    key = (r_type, str(r_id))
                    all_unique_resources[key] = (r_type, r_data)

        print(f"[BULK EXPORT] Total unique resources after fetching: {len(all_unique_resources)}")
        
        # 2. Process support files IN PARALLEL (OPTIMIZATION: 2-3x speedup, rate-limited)
        print("[BULK EXPORT] Starting support file processing...")
        async def process_single_support_file(r_type, r_id_str, orig_type, r_data):
            """Helper to process a single support file with error handling and rate limiting."""
            async with semaphore:  # Reuse same semaphore for rate limiting
                r_id = int(r_id_str) if r_id_str.isdigit() else None
                if r_id is None:
                    return
                
                try:
                    if orig_type == 'scripts':
                        await support_handler.process_script(r_id, r_data)
                    elif orig_type == 'config-profiles':
                        await support_handler.process_config_profile(r_id, r_data)
                except Exception as e:
                    print(f"Error processing support file for {orig_type} {r_id}: {e}")
        
        # Process all support files in parallel
        support_tasks = [
            process_single_support_file(r_type, r_id_str, orig_type, r_data)
            for (r_type, r_id_str), (orig_type, r_data) in all_unique_resources.items()
            if orig_type in ('scripts', 'config-profiles')
        ]
        
        if support_tasks:
            await asyncio.gather(*support_tasks, return_exceptions=True)
        print(f"[BULK EXPORT] Support file processing complete")


        # 3. Prepare for sorting
        print(f"[BULK EXPORT] Preparing resources for sorting...")
        resources_by_type = defaultdict(list)

        # Computer groups (smart and static)
        print(f"[BULK EXPORT] Fetching computer groups...")
        all_computer_groups = await client.get_all_computer_groups()
        
        # Filter out static groups (not supported by terraform-provider-jamfpro)
        static_groups = [g for g in all_computer_groups if not g.get('is_smart', False)]
        smart_groups = [g for g in all_computer_groups if g.get('is_smart', False)]
        
        if static_groups:
            print(f"[BULK EXPORT] Skipping {len(static_groups)} static group(s) (not supported by provider)")
        
        resources_by_type['smart-groups'] = smart_groups
        resources_by_type['_static_groups_skipped'] = len(static_groups)  # Track for validation report

        # Extension Attributes
        print(f"[BULK EXPORT] Fetching computer extension attributes...")
        extension_attributes = await client.list_computer_extension_attributes()
        
        # Fetch details for each EA (parallel)
        async def fetch_ea_detail(ea):
            try:
                return await client.get_computer_extension_attribute_detail(ea['id'])
            except Exception as e:
                print(f"Error fetching EA {ea['id']}: {e}")
                return None

        ea_tasks = [fetch_ea_detail(ea) for ea in extension_attributes]
        ea_details = await asyncio.gather(*ea_tasks)
        resources_by_type['extension-attributes'] = [ea for ea in ea_details if ea]
        print(f"[BULK EXPORT] Fetched {len(resources_by_type['extension-attributes'])} extension attributes")

        # Advanced Computer Searches
        print(f"[BULK EXPORT] Fetching advanced computer searches...")
        adv_searches = await client.list_advanced_computer_searches()
        async def fetch_search_detail(s):
            try:
                return await client.get_advanced_computer_search_detail(s['id'])
            except Exception as e:
                print(f"Error fetching search {s['id']}: {e}")
                return None
        search_tasks = [fetch_search_detail(s) for s in adv_searches]
        search_details = await asyncio.gather(*search_tasks)
        resources_by_type['advanced-computer-searches'] = [s for s in search_details if s]
        print(f"[BULK EXPORT] Fetched {len(resources_by_type['advanced-computer-searches'])} advanced searches")

        # Departments
        print(f"[BULK EXPORT] Fetching departments...")
        departments = await client.list_departments()
        async def fetch_dept_detail(d):
            try:
                return await client.get_department_detail(d['id'])
            except Exception as e:
                print(f"Error fetching department {d['id']}: {e}")
                return None
        dept_tasks = [fetch_dept_detail(d) for d in departments]
        dept_details = await asyncio.gather(*dept_tasks)
        resources_by_type['departments'] = [d for d in dept_details if d]
        print(f"[BULK EXPORT] Fetched {len(resources_by_type['departments'])} departments")

        # Network Segments
        print(f"[BULK EXPORT] Fetching network segments...")
        segments = await client.list_network_segments()
        async def fetch_segment_detail(s):
            try:
                return await client.get_network_segment_detail(s['id'])
            except Exception as e:
                print(f"Error fetching network segment {s['id']}: {e}")
                return None
        segment_tasks = [fetch_segment_detail(s) for s in segments]
        segment_details = await asyncio.gather(*segment_tasks)
        resources_by_type['network-segments'] = [s for s in segment_details if s]
        print(f"[BULK EXPORT] Fetched {len(resources_by_type['network-segments'])} network segments")

        for (r_type, _), (orig_type, r_data) in all_unique_resources.items():
            # Skip resources we've already fetched manually with full details
            # This also prevents static-groups from being added back after we explicitly filtered them
            if orig_type in ['smart-groups', 'static-groups', 'computer_groups', 
                           'extension-attributes', 'advanced-computer-searches', 
                           'departments', 'network-segments']:
                continue
            resources_by_type[orig_type].append(r_data)

        # 4. Topological Sort
        print(f"[BULK EXPORT] Running topological sort...")
        sorted_tuples = resolver.topological_sort(resources_by_type)
        print(f"[BULK EXPORT] Topological sort complete: {len(sorted_tuples)} resources")
        
        # 5. Organize content by file type
        print(f"[BULK EXPORT] Generating HCL...")
        files_content = defaultdict(list)
        
        for r_type, r_data in sorted_tuples:
            try:
                chunk = hcl_gen.generate_resource_hcl(r_type, r_data)
                filename = f"{r_type}.tf"
                files_content[filename].append(chunk)
            except Exception as e:
                # Log which resource failed but continue
                r_id = r_data.get('id') or r_data.get('general', {}).get('id', 'unknown')
                print(f"[ERROR] Failed to generate HCL for {r_type} ID {r_id}: {e}")
                import traceback
                traceback.print_exc()
                # Continue with other resources
        print(f"[BULK EXPORT] HCL generation complete: {len(files_content)} files")

        # 6. Create ZIP with support files
        print(f"[BULK EXPORT] Creating ZIP file...")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Write resource HCL files
            for filename, blocks in files_content.items():
                content = "\n\n".join(blocks)
                zip_file.writestr(filename, content)
            
            # Write support files (scripts and profiles)
            support_files_count = support_handler.write_files_to_zip(zip_file)
            
            # Create empty packages directory with .gitkeep for users to add packages
            zip_file.writestr("support_files/packages/.gitkeep", 
                            "# Place package files (.pkg, .dmg) here\n")
            
            # Validate export before packaging
            validator = ExportValidator()
            validation_result = validator.validate_export(
                resources_by_type=resources_by_type,
                support_handler=support_handler
            )
            
            # Add static groups count to validation result
            validation_result['_static_groups_skipped'] = resources_by_type.get('_static_groups_skipped', 0)
            
            # Generate validation report
            validation_report = generate_validation_report(validation_result)
            
            # Write provider configuration            # Generate provider.tf
            instance_url = request.credentials.url
            # Ensure https:// prefix
            if not instance_url.startswith('http'):
                instance_url = f'https://{instance_url}'
            
            provider_hcl = f"""terraform {{
  required_providers {{
    jamfpro = {{
      source  = "deploymenttheory/jamfpro"
      version = "{PROVIDER_VERSION}"
    }}
  }}
}}

provider "jamfpro" {{
  jamfpro_instance_fqdn = "{instance_url}"
  auth_method           = "basic"
  # Authentication - configure via environment variables:
  # export JAMFPRO_BASIC_USERNAME="your-username"
  # export JAMFPRO_BASIC_PASSWORD="your-password"
  # Or use client credentials:
  # export JAMFPRO_CLIENT_ID="your-client-id"
  # export JAMFPRO_CLIENT_SECRET="your-client-secret"
}}
"""
            zip_file.writestr("provider.tf", provider_hcl)
            
            # Write validation report
            zip_file.writestr("VALIDATION_REPORT.md", validation_report)
            
            # Add mobileconfig converter utility script
            converter_script_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'mobileconfig_converter.sh')
            if os.path.exists(converter_script_path):
                with open(converter_script_path, 'r') as f:
                    zip_file.writestr("utils/mobileconfig_converter.sh", f.read())
                print(f"[BULK EXPORT] Added mobileconfig converter utility")
            
            # Get summary of support files
            support_summary = support_handler.get_files_summary()
            
            # Build README with support files info
            readme = f'''# Jamf Pro Terraform Export

Generated by JamfTerraform Proporter.

## Quick Start

1. **Configure Authentication**
   
   Set environment variables for authentication:
   ```bash
   export JAMFPRO_BASIC_AUTH_USERNAME="your-username"
   export JAMFPRO_BASIC_AUTH_PASSWORD="your-password"
   ```
   
   Or use client credentials:
   ```bash
   export JAMFPRO_CLIENT_ID="your-client-id"
   export JAMFPRO_CLIENT_SECRET="your-client-secret"
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review the Plan**
   ```bash
   terraform plan
   ```

4. **Apply Changes**
   ```bash
   terraform apply
   ```

## Support Files

This export includes {support_summary['total_count']} support files:

### Scripts ({len(support_summary['scripts'])} files)
{chr(10).join([f"- `{s['path']}`" for s in support_summary['scripts']]) or "- None"}

### Configuration Profiles ({len(support_summary['profiles'])} files)
{chr(10).join([f"- `{p['path']}`" for p in support_summary['profiles']]) or "- None"}

### Packages

Package files (.pkg, .dmg) are **not** automatically downloaded due to their large size.
You must manually obtain package files from your Jamf Pro server and place them in:
`support_files/packages/`

## File Structure

```
.
├── provider.tf          # Terraform provider configuration
├── categories.tf        # Category resources
├── scripts.tf           # Script resources
├── packages.tf          # Package resources
├── config-profiles.tf   # Configuration profile resources
├── policies.tf          # Policy resources
├── README.md            # This file
└── support_files/
    ├── scripts/         # Script files (.sh, .zsh, .py, etc.)
    ├── profiles/        # Configuration profiles (.mobileconfig)
    └── packages/        # Place package files here manually
```

## Notes

- Scripts and configuration profiles use `file()` references to local files
- This ensures proper handling of special characters and multi-line content
- All resources maintain their dependency relationships via Terraform references
'''
            zip_file.writestr("README.md", readme)

        zip_buffer.seek(0)
        
        # Return ZIP file with proper filename
        instance_name = request.credentials.url.replace('https://', '').replace('http://', '').split('.')[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"jamf_terraform_{instance_name}_{timestamp}.zip"
        
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
