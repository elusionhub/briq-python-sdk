"""Briq SMS SDK for Python.

A modern Python SDK for the Briq SMS API with full async support and type safety.
"""

__version__ = "0.0.2"
__author__ = "Elution Hub"
__email__ = "elusion.lab@gmail.com"

from elusion.briq.client import BriqClient as Briq
from elusion.briq.exceptions import (
    BriqError,
    BriqAPIError,
    BriqAuthenticationError,
    BriqRateLimitError,
    BriqValidationError,
    BriqNetworkError,
)
from elusion.briq.models.campaign import Campaign, NewCampaign, UpdateCampaign
from elusion.briq.models.message import (
    Message,
    InstantMessage,
    MessageLog,
    MessageStatus,
)
from elusion.briq.models.workspace import Workspace, WorkspaceCreate, WorkspaceUpdate

__all__ = [
    # Main client
    "Briq",
    # Exceptions
    "BriqError",
    "BriqAPIError",
    "BriqAuthenticationError",
    "BriqRateLimitError",
    "BriqValidationError",
    "BriqNetworkError",
    # Models
    "Campaign",
    "NewCampaign",
    "UpdateCampaign",
    "Message",
    "InstantMessage",
    "MessageLog",
    "MessageStatus",
    "Workspace",
    "WorkspaceCreate",
    "WorkspaceUpdate",
]
