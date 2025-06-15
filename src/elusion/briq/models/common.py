"""Common models and types used across the Briq SDK."""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""

    success: bool = Field(..., description="Whether the request was successful")
    data: T = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if applicable")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""

    data: List[T] = Field(..., description="List of items")
    pagination: "PaginationInfo" = Field(..., description="Pagination information")


class PaginationInfo(BaseModel):
    """Pagination metadata."""

    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")

    @classmethod
    def __get_validators__(cls):
        yield cls._calculate_pagination_fields

    @classmethod
    def _calculate_pagination_fields(cls, values: Dict[str, Any]) -> "PaginationInfo":
        """Calculate total_pages, has_next, and has_prev based on other fields."""
        total = values.get("total", 0)
        limit = values.get("limit", 1)
        page = values.get("page", 1)

        total_pages = (total + limit - 1) // limit if total > 0 else 0
        has_next = page < total_pages
        has_prev = page > 1

        values["total_pages"] = total_pages
        values["has_next"] = has_next
        values["has_prev"] = has_prev

        return cls(**values)


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""

    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ErrorDetail(BaseModel):
    """Detailed error information."""

    field: Optional[str] = Field(None, description="Field that caused the error")
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")


class ValidationError(BaseModel):
    """Validation error response."""

    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="General error message")
    errors: List["ErrorDetail"] = Field(  # type: ignore
        default_factory=list, description="Detailed validation errors"
    )


# Query parameter models
class BaseListParams(BaseModel):
    """Base parameters for list operations."""

    page: Optional[int] = Field(1, ge=1, description="Page number")
    limit: Optional[int] = Field(50, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(None, description="Field to sort by")


MESSAGE_STATUSES = ["pending", "sent", "delivered", "failed", "cancelled"]
CAMPAIGN_STATUSES = ["draft", "scheduled", "active", "paused", "completed", "cancelled"]
