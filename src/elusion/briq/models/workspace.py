"""Workspace-related models for the Briq SDK."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

from elusion.briq.models.common import BaseListParams


class WorkspaceBase(BaseModel):
    """Base workspace model with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Workspace name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Workspace description"
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate workspace name."""
        if not v.strip():
            raise ValueError("Workspace name cannot be empty or whitespace only")
        return v.strip()

    @field_validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate workspace description."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class WorkspaceCreate(WorkspaceBase):
    """Model for creating a new workspace."""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My SMS Project",
                "description": "Workspace for managing SMS campaigns for my project",
            }
        }


class WorkspaceUpdate(BaseModel):
    """Model for updating an existing workspace."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Workspace name"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Workspace description"
    )

    @field_validator("name")
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate workspace name."""
        if v is not None:
            if not v.strip():
                raise ValueError("Workspace name cannot be empty or whitespace only")
            return v.strip()
        return v

    @field_validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate workspace description."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Project Name",
                "description": "Updated description for the workspace",
            }
        }


class Workspace(WorkspaceBase):
    """Complete workspace model with all fields."""

    user_id: Optional[str] = Field(
        None, description="ID of the user who created the workspace"
    )
    workspace_id: str = Field(..., description="Unique identifier for the workspace")

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "success": True,
                "workspace_id": "workspace-123",
                "user_id": "user-456",
                "name": "My SMS Project",
                "description": "Workspace for managing SMS campaigns for my project",
                "created_at": "2023-10-01T12:00:00Z",
            }
        }


class WorkspaceListParams(BaseListParams):
    """Parameters for listing workspaces."""

    name: Optional[str] = Field(
        None, description="Filter by workspace name (partial match)"
    )

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {"page": 1, "limit": 50, "name": "project"}
        }
