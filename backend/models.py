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
