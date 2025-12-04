"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field


class GenerateHCLRequest(BaseModel):
    """Request model for HCL generation."""
    prompt: str = Field(..., description="User prompt describing the desired Jamf configuration")
    context: str | None = Field(None, description="Optional context or existing configuration")
    scope_confirmation: str | None = Field(None, description="User's scope confirmation (yes/no/specific targeting)")


class GenerateHCLResponse(BaseModel):
    """Response model for HCL generation."""
    hcl: str = Field("", description="Generated HCL configuration")
    success: bool = Field(True, description="Whether generation was successful")
    error: str | None = Field(None, description="Error message if generation failed")
    requires_confirmation: bool = Field(False, description="Whether scope confirmation is needed")
    confirmation_message: str | None = Field(None, description="Message asking for scope confirmation")

