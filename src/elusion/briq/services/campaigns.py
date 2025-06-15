"""Campaign service for the Briq SDK."""

from typing import Dict, List, Union

from elusion.briq.models.campaign import (
    Campaign,
    NewCampaign,
    CampaignListParams,
    UpdateCampaign,
)
from elusion.briq.models.common import APIResponse
from elusion.briq.services.base import BaseService


class CampaignService(BaseService):
    """Service for managing campaigns."""

    # Async methods
    async def create(
        self, campaign_data: Union[NewCampaign, Dict[str, str]]
    ) -> APIResponse[Campaign]:
        """Create a new campaign.

        Args:
            campaign_data: Campaign creation data.

        Returns:
            Created campaign.

        Examples:
            >>> async with briq_client:
            ...     campaign = await briq_client.campaigns.create({
            ...         "name": "Summer Sale",
            ...         "description": "Promotional campaign for summer sale",
            ...         "workspace_id": "workspace-123",
            ...         "launch_date": "2025-07-01T10:00:00Z"
            ...     })
            ...     print(f"Created campaign: {campaign.data.id}")
        """
        return await self._create("create-campaign", campaign_data, Campaign)

    async def list(
        self, params: Union[CampaignListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[Campaign]]:
        """List campaigns.

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of campaigns.

        Examples:
            >>> async with briq_client:
            ...     campaigns = await briq_client.campaigns.list({
            ...         "workspace_id": "workspace-123",
            ...         "status": "active"
            ...     })
            ...     for campaign in campaigns.data:
            ...         print(f"Campaign: {campaign.name}")
        """
        if isinstance(params, dict):
            params = CampaignListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return await self._list("all-campaigns", Campaign, params)

    async def get_by_id(self, campaign_id: str) -> APIResponse[Campaign]:
        """Get a campaign by its ID.

        Args:
            campaign_id: The campaign ID.

        Returns:
            Campaign details.

        Examples:
            >>> async with briq_client:
            ...     campaign = await briq_client.campaigns.get_by_id("campaign-123")
            ...     print(f"Campaign: {campaign.data.name}")
            ...     print(f"Status: {campaign.data.status}")
            ...     print(f"Delivery rate: {campaign.data.delivery_rate}%")
        """
        return await self._get("get-campaign", Campaign, campaign_id)

    async def update(
        self, campaign_id: str, campaign_data: Union[UpdateCampaign, Dict[str, str]]
    ) -> APIResponse[Campaign]:
        """Update an existing campaign.

        Args:
            campaign_id: The campaign ID to update.
            campaign_data: Updated campaign data.

        Returns:
            Updated campaign.

        Examples:
            >>> async with briq_client:
            ...     updated_campaign = await briq_client.campaigns.update(
            ...         "campaign-123",
            ...         {
            ...             "name": "Updated Campaign Name",
            ...             "status": "scheduled",
            ...             "launch_date": "2025-07-15T10:00:00Z"
            ...         }
            ...     )
            ...     print(f"Updated: {updated_campaign.data.name}")
        """
        return await self._update(
            "update-campaign", campaign_id, campaign_data, Campaign
        )

    async def delete(self, campaign_id: str) -> APIResponse[Dict[str, bool]]:
        """Delete a campaign.

        Args:
            campaign_id: The campaign ID to delete.

        Returns:
            Deletion confirmation.

        Examples:
            >>> async with briq_client:
            ...     result = await briq_client.campaigns.delete("campaign-123")
            ...     print(f"Deleted: {result.data['deleted']}")
        """
        return await self._delete("campaigns", campaign_id)

    async def pause(self, campaign_id: str) -> APIResponse[Campaign]:
        """Pause a running campaign.

        Args:
            campaign_id: The campaign ID to pause.

        Returns:
            Updated campaign with paused status.

        Examples:
            >>> async with briq_client:
            ...     paused_campaign = await briq_client.campaigns.pause("campaign-123")
            ...     print(f"Campaign paused: {paused_campaign.data.status}")
        """
        return await self.update(campaign_id, {"status": "paused"})

    async def resume(self, campaign_id: str) -> APIResponse[Campaign]:
        """Resume a paused campaign.

        Args:
            campaign_id: The campaign ID to resume.

        Returns:
            Updated campaign with active status.

        Examples:
            >>> async with briq_client:
            ...     resumed_campaign = await briq_client.campaigns.resume("campaign-123")
            ...     print(f"Campaign resumed: {resumed_campaign.data.status}")
        """
        return await self.update(campaign_id, {"status": "active"})

    async def cancel(self, campaign_id: str) -> APIResponse[Campaign]:
        """Cancel a campaign.

        Args:
            campaign_id: The campaign ID to cancel.

        Returns:
            Updated campaign with cancelled status.

        Examples:
            >>> async with briq_client:
            ...     cancelled_campaign = await briq_client.campaigns.cancel("campaign-123")
            ...     print(f"Campaign cancelled: {cancelled_campaign.data.status}")
        """
        return await self.update(campaign_id, {"status": "cancelled"})

    # Sync methods
    def create_sync(
        self, campaign_data: Union[NewCampaign, Dict[str, str]]
    ) -> APIResponse[Campaign]:
        """Create a new campaign (sync version).

        Args:
            campaign_data: Campaign creation data.

        Returns:
            Created campaign.
        """
        return self._create_sync("campaigns", campaign_data, Campaign)

    def list_sync(
        self, params: Union[CampaignListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[Campaign]]:
        """List campaigns (sync version).

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of campaigns.
        """
        if isinstance(params, dict):
            params = CampaignListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return self._list_sync("campaigns", Campaign, params)

    def get_by_id_sync(self, campaign_id: str) -> APIResponse[Campaign]:
        """Get a campaign by its ID (sync version).

        Args:
            campaign_id: The campaign ID.

        Returns:
            Campaign details.
        """
        return self._get_sync("campaigns", Campaign, campaign_id)

    def update_sync(
        self, campaign_id: str, campaign_data: Union[UpdateCampaign, Dict[str, str]]
    ) -> APIResponse[Campaign]:
        """Update an existing campaign (sync version).

        Args:
            campaign_id: The campaign ID to update.
            campaign_data: Updated campaign data.

        Returns:
            Updated campaign.
        """
        return self._update_sync("campaigns", campaign_id, campaign_data, Campaign)

    def delete_sync(self, campaign_id: str) -> APIResponse[Dict[str, bool]]:
        """Delete a campaign (sync version).

        Args:
            campaign_id: The campaign ID to delete.

        Returns:
            Deletion confirmation.
        """
        return self._delete_sync("campaigns", campaign_id)

    def pause_sync(self, campaign_id: str) -> APIResponse[Campaign]:
        """Pause a running campaign (sync version).

        Args:
            campaign_id: The campaign ID to pause.

        Returns:
            Updated campaign with paused status.
        """
        return self.update_sync(campaign_id, {"status": "paused"})

    def resume_sync(self, campaign_id: str) -> APIResponse[Campaign]:
        """Resume a paused campaign (sync version).

        Args:
            campaign_id: The campaign ID to resume.

        Returns:
            Updated campaign with active status.
        """
        return self.update_sync(campaign_id, {"status": "active"})

    def cancel_sync(self, campaign_id: str) -> APIResponse[Campaign]:
        """Cancel a campaign (sync version).

        Args:
            campaign_id: The campaign ID to cancel.

        Returns:
            Updated campaign with cancelled status.
        """
        return self.update_sync(campaign_id, {"status": "cancelled"})
