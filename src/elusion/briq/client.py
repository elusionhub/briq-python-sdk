"""Main Briq SDK client."""

import logging
from typing import Any, Dict, Optional
from types import TracebackType

from elusion.briq.config import BriqConfig
from elusion.briq.http import HTTPClient
from elusion.briq.services import CampaignService, MessageService, WorkspaceService

logger = logging.getLogger(__name__)


class BriqClient:
    """Main client for the Briq SMS API.

    This client provides access to all Briq SMS API services including
    workspaces, campaigns, and messages. It supports both async and sync operations.

    Examples:
        >>> # Async usage (recommended)
        >>> import asyncio
        >>> from briq import Briq
        >>>
        >>> async def main():
        ...     async with Briq(api_key="your-api-key") as client:
        ...         # Test connection
        ...         is_connected = await client.test_connection()
        ...         print(f"Connected: {is_connected}")
        ...
        ...         # Send a message
        ...         response = await client.messages.send_instant({
        ...             "recipients": ["255781588379"],
        ...             "content": "Hello from Briq!",
        ...             "sender_id": "BRIQ"
        ...         })
        ...         print(f"Message sent: {response.data.status}")
        >>>
        >>> asyncio.run(main())

        >>> # Sync usage
        >>> from briq import Briq
        >>>
        >>> with Briq(api_key="your-api-key") as client:
        ...     workspaces = client.workspaces.list_sync()
        ...     for workspace in workspaces.data:
        ...         print(f"Workspace: {workspace.name}")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the Briq client.

        Args:
            api_key: Briq API key. If not provided, will try to get from BRIQ_API_KEY env var.
            base_url: Base URL for the Briq API. Defaults to https://karibu.briq.tz.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Maximum number of retries for failed requests. Defaults to 3.
            retry_delay: Delay between retries in seconds. Defaults to 1.0.
            headers: Additional headers to include in all requests.

        Raises:
            ValueError: If API key is not provided and not found in environment.

        Examples:
            >>> # Basic initialization
            >>> client = Briq(api_key="your-api-key")

            >>> # With custom configuration
            >>> client = Briq(
            ...     api_key="your-api-key",
            ...     base_url="https://custom-api.example.com",
            ...     timeout=60,
            ...     headers={"X-Custom-Header": "value"}
            ... )

            >>> # Using environment variable for API key
            >>> import os
            >>> os.environ["BRIQ_API_KEY"] = "your-api-key"
            >>> client = Briq()  # Will use API key from environment
        """
        self.config = BriqConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            headers=headers,
        )

        # Initialize HTTP client
        self.http_client = HTTPClient(self.config)

        # Initialize services
        self.workspaces = WorkspaceService(self.http_client, self.config)
        self.campaigns = CampaignService(self.http_client, self.config)
        self.messages = MessageService(self.http_client, self.config)

        logger.info(f"Briq client initialized with base URL: {self.config.base_url}")

    async def __aenter__(self) -> "BriqClient":
        """Async context manager entry."""
        await self.http_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Async context manager exit."""
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)

    def __enter__(self) -> "BriqClient":
        """Sync context manager entry."""
        self.http_client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional["TracebackType"],
    ) -> None:
        """Sync context manager exit."""
        self.http_client.__exit__(exc_type, exc_val, exc_tb)
        self.http_client.__exit__(exc_type, exc_val, exc_tb)

    async def test_connection(self) -> bool:
        """Test the connection to the Briq API.

        Returns:
            True if connection is successful, False otherwise.

        Examples:
            >>> async with Briq(api_key="your-api-key") as client:
            ...     is_connected = await client.test_connection()
            ...     if is_connected:
            ...         print("Successfully connected to Briq API")
            ...     else:
            ...         print("Failed to connect to Briq API")
        """
        try:
            url = self.config.get_endpoint_url("all-workspaces")
            response_data: Dict[str, Any] = await self.http_client.get(url)
            if not response_data:
                return False
            if isinstance(response_data, list):
                return True

            return False

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def test_connection_sync(self) -> bool:
        """Test the connection to the Briq API (sync version).

        Returns:
            True if connection is successful, False otherwise.

        Examples:
            >>> with Briq(api_key="your-api-key") as client:
            ...     is_connected = client.test_connection_sync()
            ...     if is_connected:
            ...         print("Successfully connected to Briq API")
        """
        try:
            url = self.config.get_endpoint_url("health")
            response_data: Dict[str, Any] = self.http_client.get_sync(url)
            if not response_data:
                return False
            if isinstance(response_data, list):
                return True

            return False

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def close(self) -> None:
        """Close the HTTP client and clean up resources.

        Examples:
            >>> client = Briq(api_key="your-api-key")
            >>> # ... use client
            >>> await client.close()  # Clean up when done
        """
        await self.http_client.close()
        logger.info("Briq client closed")

    def close_sync(self) -> None:
        """Close the HTTP client and clean up resources (sync version).

        Examples:
            >>> client = Briq(api_key="your-api-key")
            >>> # ... use client
            >>> client.close_sync()  # Clean up when done
        """
        self.http_client.close_sync()
        logger.info("Briq client closed")


Briq = BriqClient
