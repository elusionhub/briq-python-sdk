"""Campaign-related models for the Briq SDK."""

from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, field_validator

from elusion.briq.models.common import BaseListParams, CAMPAIGN_STATUSES


class CampaignBase(BaseModel):
    """Base campaign model with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Campaign name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Campaign description"
    )
    workspace_id: str = Field(
        ..., description="ID of the workspace this campaign belongs to"
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate campaign name."""
        if not v.strip():
            raise ValueError("Campaign name cannot be empty or whitespace only")
        return v.strip()

    @field_validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate campaign description."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class NewCampaign(CampaignBase):
    """Model for creating a new campaign."""

    launch_date: Optional[Union[datetime, str]] = Field(
        None, description="Scheduled launch date for the campaign"
    )

    @field_validator("launch_date", mode="before")
    def parse_launch_date(cls, v: Union[str, datetime, None]) -> Optional[datetime]:
        """Parse launch date from string if necessary."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid launch date format: {v}")
        return v

    @field_validator("launch_date")
    def validate_launch_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate that launch date is in the future."""
        if v is not None and v <= datetime.now(v.tzinfo):
            raise ValueError("Launch date must be in the future")
        return v

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        if isinstance(data.get("launch_date"), datetime):
            data["launch_date"] = data["launch_date"].isoformat()
        return data

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Summer Sale Campaign",
                "description": "Promotional campaign for summer sale",
                "workspace_id": "466e6a77-6f38-4b51-afbb-4b63ebf4ff43",
                "launch_date": "2025-07-01T10:00:00Z",
            }
        }
    }


class UpdateCampaign(BaseModel):
    """Model for updating an existing campaign."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Campaign name"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Campaign description"
    )
    launch_date: Optional[Union[datetime, str]] = Field(
        None, description="Scheduled launch date for the campaign"
    )

    @field_validator("name")
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate campaign name."""
        if v is not None:
            if not v.strip():
                raise ValueError("Campaign name cannot be empty or whitespace only")
            return v.strip()
        return v

    @field_validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate campaign description."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v

    @field_validator("launch_date", mode="before")
    def parse_launch_date(cls, v: Union[str, datetime, None]) -> Union[datetime, None]:
        """Parse launch date from string if necessary."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid launch date format: {v}")
        return v

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        if isinstance(data.get("launch_date"), datetime):
            data["launch_date"] = data["launch_date"].isoformat()
        return data

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Campaign Name",
                "description": "Updated campaign description",
                "launch_date": "2025-07-15T10:00:00Z",
            }
        }


class Campaign(CampaignBase):
    """Complete campaign model with all fields."""

    campaign_id: Optional[str]

    launch_date: Optional[datetime] = Field(None, description="Scheduled launch date")
    status: str = Field("draft", description="Current campaign status")

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate campaign status."""
        if v not in CAMPAIGN_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(CAMPAIGN_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "id": "4ab33b66-2207-4f82-817d-2f9779888ee7",
                "name": "Summer Sale Campaign",
                "description": "Promotional campaign for summer sale",
                "workspace_id": "466e6a77-6f38-4b51-afbb-4b63ebf4ff43",
                "launch_date": "2025-07-01T10:00:00Z",
                "status": "scheduled",
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T12:30:00Z",
            }
        }


class CampaignListParams(BaseListParams):
    """Parameters for listing campaigns."""

    workspace_id: Optional[str] = Field(None, description="Filter by workspace ID")
    status: Optional[str] = Field(None, description="Filter by campaign status")
    name: Optional[str] = Field(
        None, description="Filter by campaign name (partial match)"
    )

    @field_validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate campaign status filter."""
        if v is not None and v not in CAMPAIGN_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(CAMPAIGN_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "page": 1,
                "limit": 50,
                "workspace_id": "466e6a77-6f38-4b51-afbb-4b63ebf4ff43",
                "status": "active",
                "sort_by": "launch_date",
                "sort_order": "desc",
            }
        }
