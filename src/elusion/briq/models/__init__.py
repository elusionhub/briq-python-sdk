"""Briq SDK data models."""

from elusion.briq.models.campaign import (
    Campaign,
    NewCampaign,
    CampaignListParams,
    UpdateCampaign,
)
from elusion.briq.models.common import (
    APIResponse,
    BaseListParams,
    ErrorDetail,
    PaginatedResponse,
    PaginationInfo,
    ValidationError,
)
from elusion.briq.models.message import (
    CampaignMessage,
    InstantMessage,
    Message,
    MessageListParams,
    MessageLog,
    MessageLogParams,
    MessageStatus,
    MessageResponse,
    MessageHistory,
)
from elusion.briq.models.workspace import (
    Workspace,
    WorkspaceCreate,
    WorkspaceListParams,
    WorkspaceUpdate,
)

__all__ = [
    # Common models
    "APIResponse",
    "PaginatedResponse",
    "PaginationInfo",
    "BaseListParams",
    "ErrorDetail",
    "ValidationError",
    # Workspace models
    "Workspace",
    "WorkspaceCreate",
    "WorkspaceUpdate",
    "WorkspaceListParams",
    # Campaign models
    "Campaign",
    "NewCampaign",
    "UpdateCampaign",
    "CampaignListParams",
    # Message models
    "Message",
    "InstantMessage",
    "MessageResponse",
    "CampaignMessage",
    "MessageStatus",
    "MessageLog",
    "MessageListParams",
    "MessageLogParams",
    "MessageHistory",
]
