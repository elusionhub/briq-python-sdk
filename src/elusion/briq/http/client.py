"""HTTP client for the Briq SDK."""

import json
import logging
from typing import Any, Dict, Optional, Union

import httpx

from elusion.briq.config import BriqConfig
from elusion.briq.exceptions import (
    BriqNetworkError,
    BriqTimeoutError,
    create_api_error,
)

logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client for making requests to the Briq API."""

    def __init__(self, config: BriqConfig) -> None:
        """Initialize the HTTP client.

        Args:
            config: Briq configuration instance.
        """
        self.config = config
        self._client: Optional[httpx.AsyncClient] = None
        self._sync_client: Optional[httpx.Client] = None

    async def __aenter__(self) -> "HTTPClient":
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    def __enter__(self) -> "HTTPClient":
        """Sync context manager entry."""
        self._ensure_sync_client()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Sync context manager exit."""
        self.close_sync()

    async def _ensure_client(self) -> None:
        """Ensure async client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.config.timeout,
                headers=self.config.headers.copy(),
            )

    def _ensure_sync_client(self) -> None:
        """Ensure sync client is initialized."""
        if self._sync_client is None:
            self._sync_client = httpx.Client(
                timeout=self.config.timeout,
                headers=self.config.headers.copy(),
            )

    async def close(self) -> None:
        """Close the async HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def close_sync(self) -> None:
        """Close the sync HTTP client."""
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make an async HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            url: Request URL.
            params: Query parameters.
            data: Request body data.
            headers: Additional headers.
            **kwargs: Additional arguments for httpx.

        Returns:
            Parsed JSON response data.

        Raises:
            BriqAPIError: For API errors.
            BriqNetworkError: For network errors.
            BriqTimeoutError: For timeout errors.
        """
        await self._ensure_client()

        if self._client is None:
            raise BriqNetworkError("Async HTTP client is not initialized", None)

        request_headers = self.config.headers.copy()
        if headers:
            request_headers.update(headers)

        json_data = None
        if data is not None:
            if isinstance(data, dict):
                json_data = data
            else:
                json_data = json.loads(data)

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        try:
            logger.debug(f"Making {method} request to {url}")

            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=request_headers,
                **kwargs,
            )

            return await self._handle_response(response)

        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise BriqTimeoutError(
                f"Request timeout after {self.config.timeout} seconds",
                self.config.timeout,
            ) from e
        except httpx.NetworkError as e:
            logger.error(f"Network error: {e}")
            raise BriqNetworkError(f"Network error: {str(e)}", e) from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise BriqNetworkError(f"Unexpected error: {str(e)}", e) from e

    def request_sync(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make a sync HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            url: Request URL.
            params: Query parameters.
            data: Request body data.
            headers: Additional headers.
            **kwargs: Additional arguments for httpx.

        Returns:
            Parsed JSON response data.

        Raises:
            BriqAPIError: For API errors.
            BriqNetworkError: For network errors.
            BriqTimeoutError: For timeout errors.
        """
        self._ensure_sync_client()

        if self._sync_client is None:
            raise BriqNetworkError("Sync HTTP client is not initialized", None)

        request_headers = self.config.headers.copy()
        if headers:
            request_headers.update(headers)

        json_data = None
        if data is not None:
            if isinstance(data, dict):
                json_data = data
            else:
                json_data = json.loads(data)

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        try:
            logger.debug(f"Making {method} request to {url}")

            response = self._sync_client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=request_headers,
                **kwargs,
            )

            return self._handle_response_sync(response)

        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise BriqTimeoutError(
                f"Request timeout after {self.config.timeout} seconds",
                self.config.timeout,
            ) from e
        except httpx.NetworkError as e:
            logger.error(f"Network error: {e}")
            raise BriqNetworkError(f"Network error: {str(e)}", e) from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise BriqNetworkError(f"Unexpected error: {str(e)}", e) from e

    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response for async requests.

        Args:
            response: HTTP response object.

        Returns:
            Parsed response data.

        Raises:
            BriqAPIError: For API errors.
        """
        logger.debug(f"Response status: {response.status_code}")

        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response JSON: {e}")
            raise BriqNetworkError(f"Invalid JSON response: {str(e)}", e) from e

        if response.is_success:
            return response_data

        # Handle API errors
        error_message = response_data.get("error", f"HTTP {response.status_code}")
        error_code = response_data.get("code")

        logger.error(f"API error: {response.status_code} - {error_message}")

        raise create_api_error(
            status_code=response.status_code,
            message=error_message,
            response_data=response_data,
            error_code=error_code,
        )

    def _handle_response_sync(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response for sync requests.

        Args:
            response: HTTP response object.

        Returns:
            Parsed response data.

        Raises:
            BriqAPIError: For API errors.
        """
        logger.debug(f"Response status: {response.status_code}")

        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response JSON: {e}")
            raise BriqNetworkError(f"Invalid JSON response: {str(e)}", e) from e

        if response.is_success:
            return response_data

        # Handle API errors
        error_message = response_data.get("error", f"HTTP {response.status_code}")
        error_code = response_data.get("code")

        logger.error(f"API error: {response.status_code} - {error_message}")

        raise create_api_error(
            status_code=response.status_code,
            message=error_message,
            response_data=response_data,
            error_code=error_code,
        )

    async def get(
        self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", url, params=params, **kwargs)

    async def post(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", url, data=data, **kwargs)

    async def put(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", url, data=data, **kwargs)

    async def patch(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        return await self.request("PATCH", url, data=data, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", url, **kwargs)

    # Sync convenience methods
    def get_sync(
        self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a sync GET request."""
        return self.request_sync("GET", url, params=params, **kwargs)

    def post_sync(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a sync POST request."""
        return self.request_sync("POST", url, data=data, **kwargs)

    def put_sync(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a sync PUT request."""
        return self.request_sync("PUT", url, data=data, **kwargs)

    def patch_sync(
        self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make a sync PATCH request."""
        return self.request_sync("PATCH", url, data=data, **kwargs)

    def delete_sync(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a sync DELETE request."""
        return self.request_sync("DELETE", url, **kwargs)
