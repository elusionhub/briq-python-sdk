from elusion.briq import Briq
from elusion.briq.models import NewCampaign, UpdateCampaign
import asyncio


async def test_connection():
    async with Briq() as client:
        try:
            print(await client.test_connection())
        except Exception as e:
            print(f"Failed to connect to Briq API: {e}")


async def create_campaign():
    async with Briq() as client:
        try:
            campaign = NewCampaign(
                workspace_id="0854d4ef-46df-49c6-8811-7d110d1814d1",
                description="This is a test campaign",
                name="Test Campaign",
                launch_date="2025-07-01T10:00:00Z",
            )
            campaign = await client.campaigns.create(campaign)
            print(campaign.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to create campaign: {e}")


async def list_campaigns():
    async with Briq() as client:
        try:
            campaigns = await client.campaigns.list()
            print(campaigns.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to list campaigns: {e}")


async def get_campaign_by_id(campaign_id: str):
    async with Briq() as client:
        try:
            campaign = await client.campaigns.get_by_id(campaign_id)
            print(campaign.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to get campaign by ID: {e}")


async def update_campaign(campaign_id: str):
    async with Briq() as client:
        try:
            campaign = UpdateCampaign(
                description="This is an updated test campaign",
                name="Updated Test Campaign",
                launch_date="2025-07-15T10:00:00Z",
            )
            updated_campaign = await client.campaigns.update(campaign_id, campaign)
            print(updated_campaign.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to update campaign: {e}")


if __name__ == "__main__":
    # asyncio.run(test_connection())
    # asyncio.run(create_campaign())
    # asyncio.run(list_campaigns())
    # asyncio.run(get_campaign_by_id("af6217af-1f05-419d-8ae3-f995e95af4c4"))
    asyncio.run(update_campaign("af6217af-1f05-419d-8ae3-f995e95af4c4"))
