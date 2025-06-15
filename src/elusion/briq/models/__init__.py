"""Briq SDK data models."""

from elusion.briq.models.campaign import (
    Campaign,
    CampaignCreate,
    CampaignListParams,
    CampaignUpdate,
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
    CampaignMessageCreate,
    InstantMessage,
    Message,
    MessageListParams,
    MessageLog,
    MessageLogParams,
    MessageStatus,
    MessageResponse,
    MessageHistory
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
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignListParams",
    # Message models
    "Message",
    "InstantMessage",
    "MessageResponse",
    "CampaignMessageCreate",
    "MessageStatus",
    "MessageLog",
    "MessageListParams",
    "MessageLogParams",
    "MessageHistory",
]
