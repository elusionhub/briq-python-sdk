"""Workspace service for the Briq SDK."""

from typing import Dict, List, Union

from elusion.briq.models.common import APIResponse
from elusion.briq.models.workspace import (
    Workspace,
    WorkspaceCreate,
    WorkspaceListParams,
    WorkspaceUpdate,
)
from elusion.briq.services.base import BaseService


class WorkspaceService(BaseService):
    """Service for managing workspaces."""

    # Async methods
    async def create(
        self, workspace_data: Union[WorkspaceCreate, Dict[str, str]]
    ) -> APIResponse[Workspace]:
        """Create a new workspace.

        Args:
            workspace_data: Workspace creation data.

        Returns:
            Created workspace.

        Examples:
            >>> async with briq_client:
            ...     workspace = await briq_client.workspaces.create({
            ...         "name": "My Project",
            ...         "description": "SMS campaigns for my project"
            ...     })
            ...     print(f"Created workspace: {workspace.data.id}")
        """
        return await self._create("create-workspace", workspace_data, Workspace)

    async def list(
        self, params: Union[WorkspaceListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[Workspace]]:
        """List all workspaces.

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of workspaces.

        Examples:
            >>> async with briq_client:
            ...     workspaces = await briq_client.workspaces.list()
            ...     for workspace in workspaces.data:
            ...         print(f"Workspace: {workspace.name}")
        """
        if isinstance(params, dict):
            params = WorkspaceListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
                sort_by=params.get("sort_by", "created_at"),
            )
        result = await self._list("all-workspaces", Workspace, params)
        return result

    async def get_by_id(self, workspace_id: str) -> APIResponse[Workspace]:
        """Get a workspace by its ID.

        Args:
            workspace_id: The workspace ID.

        Returns:
            Workspace details.

        Examples:
            >>> async with briq_client:
            ...     workspace = await briq_client.workspaces.get_by_id("workspace-123")
            ...     print(f"Workspace: {workspace.data.name}")
        """
        return await self._get("get-workspace", Workspace, workspace_id)

    async def update(
        self, workspace_id: str, workspace_data: Union[WorkspaceUpdate, Dict[str, str]]
    ) -> APIResponse[Workspace]:
        """Update an existing workspace.

        Args:
            workspace_id: The workspace ID to update.
            workspace_data: Updated workspace data.

        Returns:
            Updated workspace.

        Examples:
            >>> async with briq_client:
            ...     updated_workspace = await briq_client.workspaces.update(
            ...         "workspace-123",
            ...         {"name": "Updated Project Name"}
            ...     )
            ...     print(f"Updated: {updated_workspace.data.name}")
        """
        return await self._update(
            "update-workspace", workspace_id, workspace_data, Workspace
        )

    async def delete(self, workspace_id: str) -> APIResponse[Dict[str, bool]]:
        """Delete a workspace.

        Args:
            workspace_id: The workspace ID to delete.

        Returns:
            Deletion confirmation.

        Examples:
            >>> async with briq_client:
            ...     result = await briq_client.workspaces.delete("workspace-123")
            ...     print(f"Deleted: {result.data['deleted']}")
        """
        return await self._delete("workspaces", workspace_id)

    # Sync methods
    def create_sync(
        self, workspace_data: Union[WorkspaceCreate, Dict[str, str]]
    ) -> APIResponse[Workspace]:
        """Create a new workspace (sync version).

        Args:
            workspace_data: Workspace creation data.

        Returns:
            Created workspace.
        """
        return self._create_sync("workspaces", workspace_data, Workspace)

    def list_sync(
        self, params: Union[WorkspaceListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[Workspace]]:
        """List all workspaces (sync version).

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of workspaces.
        """
        if isinstance(params, dict):
            params = WorkspaceListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return self._list_sync("workspaces", Workspace, params)

    def get_by_id_sync(self, workspace_id: str) -> APIResponse[Workspace]:
        """Get a workspace by its ID (sync version).

        Args:
            workspace_id: The workspace ID.

        Returns:
            Workspace details.
        """
        return self._get_sync("workspaces", Workspace, workspace_id)

    def update_sync(
        self, workspace_id: str, workspace_data: Union[WorkspaceUpdate, Dict[str, str]]
    ) -> APIResponse[Workspace]:
        """Update an existing workspace (sync version).

        Args:
            workspace_id: The workspace ID to update.
            workspace_data: Updated workspace data.

        Returns:
            Updated workspace.
        """
        return self._update_sync("workspaces", workspace_id, workspace_data, Workspace)

    def delete_sync(self, workspace_id: str) -> APIResponse[Dict[str, bool]]:
        """Delete a workspace (sync version).

        Args:
            workspace_id: The workspace ID to delete.

        Returns:
            Deletion confirmation.
        """
        return self._delete_sync("workspaces", workspace_id)
