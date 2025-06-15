from typing import Any, Dict
from elusion.briq import Briq
import asyncio


async def test_connection():
    async with Briq() as client:
        try:
            print(await client.test_connection())
        except Exception as e:
            print(f"Failed to connect to Briq API: {e}")


async def createWorkspace():
    async with Briq() as client:
        workspace_data: Dict[str, Any] = {
            "name": "New Workspace Test",
            "description": "This is a test workspace.",
        }

        try:
            response = await client.workspaces.create(workspace_data)
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to create workspace: {e}")


async def listWorkspaces():
    async with Briq() as client:
        try:
            response = await client.workspaces.list()
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to list workspaces: {e}")


async def getWorkspaceById(workspace_id: str):
    async with Briq() as client:
        try:
            response = await client.workspaces.get_by_id(workspace_id)
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to get workspace by ID: {e}")


async def updateWorkspace(workspace_id: str):
    async with Briq() as client:
        workspace_data: Dict[str, Any] = {
            "name": "Updated Workspace Name",
            "description": "This is an updated description for the workspace.",
        }

        try:
            response = await client.workspaces.update(workspace_id, workspace_data)
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to update workspace: {e}")


if __name__ == "__main__":
    # asyncio.run(test_connection())
    # asyncio.run(createWorkspace())
    # asyncio.run(listWorkspaces())
    # asyncio.run(getWorkspaceById("0854d4ef-46df-49c6-8811-7d110d1814d1"))
    asyncio.run(updateWorkspace("0854d4ef-46df-49c6-8811-7d110d1814d1"))
