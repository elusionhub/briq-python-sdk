"""Configuration and constants for the Briq SDK."""

import os
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()


# Default configuration
DEFAULT_BASE_URL = "https://karibu.briq.tz"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

# API version
API_VERSION = "v1"

# Environment variable names
ENV_API_KEY = "BRIQ_API_KEY"
ENV_BASE_URL = "BRIQ_BASE_URL"
ENV_TIMEOUT = "BRIQ_TIMEOUT"

# HTTP headers
DEFAULT_HEADERS = {
    "User-Agent": "briq-python-sdk",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": os.getenv(ENV_API_KEY, ""),
}

# Rate limiting
DEFAULT_RATE_LIMIT_RETRY_ATTEMPTS = 3
DEFAULT_RATE_LIMIT_RETRY_DELAY = 60.0  # seconds

# Endpoints
ENDPOINTS = {
    "workspaces": "/workspace",
    "all-workspaces": "/workspace/all/",
    "create-workspace": "/workspace/create/",
    "update-workspace": "/workspace/update",
    "get-workspace": "/workspace",
    "messages": "/message",
    "messages-instant": "/message/send-instant",
    "messages-logs": "/message/logs",
    "messages-history": "/message/history",
    "messages-campaign": "/message/send-campaign",
    "create-campaign": "/campaign/create/",
    "all-campaigns": "/campaign/all/",
    "get-campaign": "/campaign",
    "update-campaign": "/campaign/update",
}


class BriqConfig(object):
    """Configuration class for the Briq SDK."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize configuration.

        Args:
            api_key: Briq API key. If not provided, will try to get from environment.
            base_url: Base URL for the Briq API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            retry_delay: Delay between retries in seconds.
            headers: Additional headers to include in requests.
        """
        self.api_key = api_key or os.getenv(ENV_API_KEY)
        if not self.api_key:
            raise ValueError(
                f"API key is required. Set {ENV_API_KEY} environment variable "
                "or pass api_key parameter."
            )

        self.base_url = base_url or os.getenv(ENV_BASE_URL, DEFAULT_BASE_URL)

        # Parse timeout from environment if provided
        env_timeout = os.getenv(ENV_TIMEOUT)
        if env_timeout:
            try:
                env_timeout_float = float(env_timeout)
            except ValueError:
                env_timeout_float = DEFAULT_TIMEOUT
        else:
            env_timeout_float = DEFAULT_TIMEOUT

        self.timeout = timeout or env_timeout_float
        self.max_retries = max_retries or DEFAULT_MAX_RETRIES
        self.retry_delay = retry_delay or DEFAULT_RETRY_DELAY

        # Merge default headers with custom headers
        self.headers = DEFAULT_HEADERS.copy()
        if headers:
            self.headers.update(headers)

        # Add authorization header
        self.headers["Authorization"] = f"Bearer {self.api_key}"

    @property
    def api_url(self) -> str:
        """Get the full API URL with version."""
        return f"{self.base_url.rstrip('/')}/{API_VERSION}"

    def get_endpoint_url(self, endpoint: str) -> str:
        """Get the full URL for an endpoint.

        Args:
            endpoint: Endpoint key from ENDPOINTS dict.

        Returns:
            Full URL for the endpoint.
        """
        if endpoint not in ENDPOINTS:
            raise ValueError(f"Unknown endpoint: {endpoint}")
        return f"{self.api_url}{ENDPOINTS[endpoint]}"
