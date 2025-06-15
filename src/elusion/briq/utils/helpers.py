"""Helper utilities for the Briq SDK."""

import asyncio
import logging
from datetime import datetime, timezone
from collections.abc import Coroutine
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    """Set up logging for the Briq SDK.

    Args:
        level: Logging level to use.

    Examples:
        >>> from elusion.briq.utils import setup_logging
        >>> setup_logging(logging.DEBUG)  # Enable debug logging
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set up specific logger for briq
    briq_logger = logging.getLogger("briq")
    briq_logger.setLevel(level)


def chunk_list(items: List[T], chunk_size: int) -> List[List[T]]:
    """Split a list into chunks of specified size.

    Args:
        items: List to chunk.
        chunk_size: Size of each chunk.

    Returns:
        List of chunks.

    Examples:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def format_phone_for_display(phone: str) -> str:
    """Format a phone number for display purposes.

    Args:
        phone: Phone number to format.

    Returns:
        Formatted phone number.

    Examples:
        >>> format_phone_for_display("255781588379")
        "+255 781 588 379"
        >>> format_phone_for_display("1234567890")
        "+1 234 567 890"
    """
    if not phone:
        return ""

    # Remove any existing formatting
    digits = "".join(c for c in phone if c.isdigit())

    if not digits:
        return phone

    # Add + prefix if not present
    if not phone.startswith("+"):
        digits = "+" + digits
    else:
        digits = "+" + digits

    # Format based on length
    if len(digits) == 13:  # +XXX XXX XXX XXX (like +255 781 588 379)
        return f"{digits[:4]} {digits[4:7]} {digits[7:10]} {digits[10:]}"
    elif len(digits) == 12:  # +XX XXX XXX XXX (like +1 234 567 890)
        return f"{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"
    else:
        # Default formatting: insert spaces every 3 digits after country code
        if len(digits) > 4:
            country_code = digits[:4]
            rest = digits[4:]
            formatted_rest = " ".join([rest[i : i + 3] for i in range(0, len(rest), 3)])
            return f"{country_code} {formatted_rest}"
        else:
            return digits


def calculate_message_cost(message_length: int, cost_per_sms: float = 0.05) -> float:
    """Calculate the cost of sending a message based on its length.

    Args:
        message_length: Length of the message in characters.
        cost_per_sms: Cost per SMS segment.

    Returns:
        Total cost for the message.

    Examples:
        >>> calculate_message_cost(50)  # Single SMS
        0.05
        >>> calculate_message_cost(200)  # Multi-part SMS
        0.10
    """
    if message_length <= 0:
        return 0.0

    # Standard SMS is 160 characters, multi-part SMS segments are 153 characters each
    if message_length <= 160:
        segments = 1
    else:
        segments = (message_length - 1) // 153 + 1

    return segments * cost_per_sms


def get_current_timestamp() -> datetime:
    """Get current timestamp in UTC.

    Returns:
        Current UTC timestamp.

    Examples:
        >>> timestamp = get_current_timestamp()
        >>> print(timestamp.isoformat())
        2025-06-15T10:30:00+00:00
    """
    return datetime.now(timezone.utc)


def parse_iso_timestamp(timestamp_str: str) -> Optional[datetime]:
    """Parse an ISO format timestamp string.

    Args:
        timestamp_str: ISO format timestamp string.

    Returns:
        Parsed datetime object, or None if parsing fails.

    Examples:
        >>> parse_iso_timestamp("2025-06-15T10:30:00Z")
        datetime.datetime(2025, 6, 15, 10, 30, tzinfo=datetime.timezone.utc)
    """
    if not timestamp_str:
        return None

    try:
        # Handle different ISO format variations
        timestamp_str = timestamp_str.replace("Z", "+00:00")
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        logger.warning(f"Failed to parse timestamp: {timestamp_str}")
        return None


def safe_json_extract(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely extract nested values from a JSON-like dictionary.

    Args:
        data: Dictionary to extract from.
        *keys: Sequence of keys to navigate.
        default: Default value if extraction fails.

    Returns:
        Extracted value or default.

    Examples:
        >>> data = {"user": {"profile": {"name": "John"}}}
        >>> safe_json_extract(data, "user", "profile", "name")
        "John"
        >>> safe_json_extract(data, "user", "missing", "field", default="N/A")
        "N/A"
    """
    current = data

    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError, AttributeError):
        return default


def run_async(coro: Coroutine[Any, Any, T]) -> T:
    """Run an async coroutine in a sync context.

    Args:
        coro: Coroutine to run.

    Returns:
        Result of the coroutine.

    Examples:
        >>> async def async_function():
        ...     return "Hello"
        >>> result = run_async(async_function())
        >>> print(result)
        Hello
    """
    try:
        # Try to get the current event loop
        asyncio.get_running_loop()
        # If we're already in an event loop, we can't use asyncio.run()
        raise RuntimeError("Cannot use run_async() within an async context")
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        return asyncio.run(coro)


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data for logging purposes.

    Args:
        data: Sensitive data to mask.
        visible_chars: Number of characters to leave visible.

    Returns:
        Masked data string.

    Examples:
        >>> mask_sensitive_data("sk_1234567890abcdef")
        "sk_1****"
        >>> mask_sensitive_data("secret123", visible_chars=2)
        "se****"
    """
    if not data or len(data) <= visible_chars:
        return "*" * len(data) if data else ""

    visible = data[:visible_chars]
    masked = "*" * (len(data) - visible_chars)
    return visible + masked


def build_user_agent(
    sdk_version: str = "0.1.0", python_version: Optional[str] = None
) -> str:
    """Build a user agent string for HTTP requests.

    Args:
        sdk_version: Version of the SDK.
        python_version: Python version string.

    Returns:
        User agent string.

    Examples:
        >>> build_user_agent("0.1.0", "3.9.0")
        "briq-python-sdk/0.1.0 Python/3.9.0"
    """
    import sys

    if python_version is None:
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    return f"briq-python-sdk/{sdk_version} Python/{python_version}"
