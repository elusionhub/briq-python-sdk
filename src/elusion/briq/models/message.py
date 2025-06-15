"""Message-related models for the Briq SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from elusion.briq.models.common import (
    BaseListParams,
    MESSAGE_STATUSES,
)


class MessageBase(BaseModel):
    """Base message model with common fields."""

    content: str = Field(
        ..., min_length=1, max_length=1600, description="Message content"
    )
    sender_id: str = Field(
        ..., max_length=11, description="Sender ID (up to 11 characters)"
    )

    @field_validator("content")
    def validate_content(cls, v: str) -> str:
        """Validate message content."""
        if not v.strip():
            raise ValueError("Message content cannot be empty or whitespace only")
        return v.strip()

    @field_validator("sender_id")
    def validate_sender_id(cls, v: str) -> str:
        """Validate sender ID format."""
        if not v.strip():
            raise ValueError("Sender ID cannot be empty")
        cleaned = "".join(c for c in v if c.isalnum())
        if len(cleaned) > 11:
            cleaned = cleaned[:11]
        return cleaned


class InstantMessage(MessageBase):
    """Model for creating instant messages."""

    recipients: List[str] = Field(description="List of recipient phone numbers")

    @field_validator("recipients")
    def validate_recipients(cls, v: List[str]) -> List[str]:
        """Validate recipient phone numbers and enforce min/max items."""
        if not v or len(v) < 1:
            raise ValueError("At least one recipient is required")
        if len(v) > 1000:
            raise ValueError("No more than 1000 recipients are allowed")

        validated_recipients: List[str] = []
        for recipient in v:
            # Basic phone number validation
            cleaned = "".join(c for c in recipient if c.isdigit() or c == "+")
            if not cleaned:
                raise ValueError(f"Invalid phone number: {recipient}")
            if len(cleaned) < 10:
                raise ValueError(f"Phone number too short: {recipient}")
            validated_recipients.append(cleaned)

        return validated_recipients

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "recipients": ["255700000000", "255700000000"],
                "content": "Hello from Briq SMS!",
                "sender_id": "BRIQ",
            }
        }


class MessageResponse(BaseModel):
    message_id: Optional[str] = Field(
        None, description="ID of the sent message (if successful)"
    )
    status: str = Field(
        "pending", description="Initial status of the message (default is 'pending')"
    )


class CampaignMessage(MessageBase):
    """Model for creating campaign messages."""

    campaign_id: str = Field(..., description="Campaign ID")
    group_id: Optional[str] = Field(None, description="Target group ID (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "campaign_id": "4ab33b66-2207-4f82-817d-2f9779888ee7",
                "group_id": "group-123",
                "content": "Special campaign offer just for you!",
                "sender_id": "BRIQ",
            }
        }


class Message(BaseModel):
    """Complete message model."""

    recipient: str = Field(..., description="Recipient phone number")
    content: str = Field(..., description="Message content")
    sender_id: str = Field(..., description="Sender ID")
    status: str = Field("pending", description="Message status")

    campaign_id: Optional[str] = Field(
        None, description="Campaign ID if sent via campaign"
    )
    group_id: Optional[str] = Field(None, description="Group ID if sent to a group")

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate message status."""
        if v not in MESSAGE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(MESSAGE_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "id": "msg-123456789",
                "recipient": "255781588379",
                "content": "Hello from Briq SMS!",
                "sender_id": "BRIQ",
                "status": "delivered",
                "campaign_id": "4ab33b66-2207-4f82-817d-2f9779888ee7",
                "created_at": "2025-06-15T10:00:00Z",
            }
        }


class MessageStatus(BaseModel):
    """Message status information."""

    id: str = Field(..., description="Message ID")
    status: str = Field(..., description="Current message status")
    recipient: str = Field(..., description="Recipient phone number")

    # Timestamps
    sent_at: Optional[datetime] = Field(None, description="When the message was sent")
    delivered_at: Optional[datetime] = Field(
        None, description="When the message was delivered"
    )
    failed_at: Optional[datetime] = Field(None, description="When the message failed")

    # Error information
    error_code: Optional[str] = Field(None, description="Error code if message failed")
    error_message: Optional[str] = Field(
        None, description="Error message if message failed"
    )

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate message status."""
        if v not in MESSAGE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(MESSAGE_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg-123456789",
                "status": "delivered",
                "recipient": "255781588379",
                "sent_at": "2025-06-15T10:00:00Z",
                "delivered_at": "2025-06-15T10:00:05Z",
            }
        }


class Log(BaseModel):
    """Message log entry."""

    log_id: str
    message_id: str
    status: str
    timestamp: str
    error_details: Optional[str] = None
    response_group_id: Optional[int | str] = None
    response_group_name: Optional[str] = None
    response_id: Optional[int | str] = None
    response_name: Optional[str] = None
    response_description: Optional[str] = None
    campaign_id: Optional[int | str] = None
    campaign_name: Optional[str] = None
    content: str
    recipient: Optional[str] = None

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate log status."""
        if v not in MESSAGE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(MESSAGE_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "msg-123456789",
                "log_id": "log-987654321",
                "status": "delivered",
                "timestamp": "2025-06-15T10:00:05Z",
                "recipient": "255781588379",
                "content": "Hello from Briq SMS!",
                "campaign_id": "4ab33b66-2207-4f82-817d-2f9779888ee7",
            }
        }


class MessageLog(BaseModel):
    user_id: str
    logs: List[Log]


class MessageHistory(BaseModel):
    """Model for message history."""

    message_id: str
    user_id: str
    recipient: List[str] | str | None
    campaign_id: Optional[str] = None
    channel_id: str
    sender_id: str
    content: str
    status: str
    sent_at: str | None


class MessageListParams(BaseListParams):
    """Parameters for listing messages."""

    status: Optional[str] = Field(None, description="Filter by message status")
    campaign_id: Optional[str] = Field(None, description="Filter by campaign ID")
    recipient: Optional[str] = Field(
        None, description="Filter by recipient phone number"
    )
    sender_id: Optional[str] = Field(None, description="Filter by sender ID")

    @field_validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status filter."""
        if v is not None and v not in MESSAGE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(MESSAGE_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "page": 1,
                "limit": 50,
                "status": "delivered",
                "campaign_id": "4ab33b66-2207-4f82-817d-2f9779888ee7",
            }
        }


class MessageLogParams(BaseListParams):
    """Parameters for fetching message logs."""

    message_id: Optional[str] = Field(None, description="Filter by specific message ID")
    status: Optional[str] = Field(None, description="Filter by log status")

    @field_validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status filter."""
        if v is not None and v not in MESSAGE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(MESSAGE_STATUSES)}"
            )
        return v

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "page": 1,
                "limit": 100,
                "message_id": "msg-123456789",
                "status": "delivered",
            }
        }
