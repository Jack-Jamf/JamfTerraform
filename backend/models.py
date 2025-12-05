"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field


class GenerateHCLRequest(BaseModel):
    """Request model for HCL generation."""
    prompt: str = Field(..., description="User prompt describing the desired Jamf configuration")
    context: str | None = Field(None, description="Optional context or existing configuration")


class GenerateHCLResponse(BaseModel):
    """Response model for HCL generation."""
    hcl: str = Field(..., description="Generated HCL configuration")
    success: bool = Field(True, description="Whether generation was successful")
    error: str | None = Field(None, description="Error message if generation failed")


class JamfCredentials(BaseModel):
    """Jamf Pro credentials."""
    url: str = Field(..., description="Jamf Pro instance URL")
    username: str = Field(..., description="API username")
    password: str = Field(..., description="API password")


class JamfResourcesRequest(BaseModel):
    """Request model for listing Jamf resources."""
    credentials: JamfCredentials = Field(..., description="Jamf Pro credentials")
    resource_type: str = Field(..., description="Type of resource to list")


class JamfResourceListResponse(BaseModel):
    """Response model for Jamf resource listing."""
    resources: list = Field(default_factory=list, description="List of resources")
    resource_type: str = Field(..., description="Type of resources returned")
    success: bool = Field(True, description="Whether fetch was successful")
    error: str | None = Field(None, description="Error message if fetch failed")


class JamfInstanceSummary(BaseModel):
    """Summary of resources in a Jamf instance."""
    resource_type: str
    count: int
    items: list  # Basic list with id/name


class JamfInstanceExportRequest(BaseModel):
    """Request to export entire Jamf instance or selected types."""
    credentials: JamfCredentials
    selected_types: list[str] = Field(default_factory=list, description="Empty = all types")


class JamfInstanceExportResponse(BaseModel):
    """Response with HCL and resource summary."""
    summary: list[JamfInstanceSummary]
    hcl: str = Field(..., description="Complete HCL file content")
    success: bool = Field(True, description="Whether export was successful")
    error: str | None = Field(None, description="Error message if export failed")


class JamfResourceDetailRequest(BaseModel):
    """Request for individual resource details."""
    credentials: JamfCredentials
    resource_type: str = Field(..., description="Type of resource (policies, scripts, etc.)")
    resource_id: int = Field(..., description="ID of the resource")


class BulkResourceIdentifier(BaseModel):
    """Identifier for a resource in bulk export."""
    type: str
    id: int


class BulkExportRequest(BaseModel):
    """Request to export multiple specific resources."""
    credentials: JamfCredentials
    resources: list[BulkResourceIdentifier]


class ResourceDependency(BaseModel):
    """A single dependency."""
    type: str = Field(..., description="Dependency type (script, package, etc.)")
    id: int
    name: str


class JamfResourceDetailResponse(BaseModel):
    """Response with resource details, dependencies, and HCL."""
    resource: dict = Field(..., description="Full resource data")
    dependencies: list[ResourceDependency] = Field(default_factory=list)
    hcl: str = Field(..., description="Generated HCL for this resource")
    bundle_hcl: str | None = Field(None, description="Complete HCL bundle with dependencies")
    success: bool = Field(True)
    error: str | None = None

