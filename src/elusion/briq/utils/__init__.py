"""Utility functions for the Briq SDK."""

from elusion.briq.utils.helpers import (
    build_user_agent,
    calculate_message_cost,
    chunk_list,
    format_phone_for_display,
    get_current_timestamp,
    mask_sensitive_data,
    parse_iso_timestamp,
    run_async,
    safe_json_extract,
    setup_logging,
)
from elusion.briq.utils.validation import (
    normalize_phone_number,
    validate_campaign_name,
    validate_message_content,
    validate_phone_number,
    validate_phone_numbers,
    validate_sender_id,
    validate_uuid,
    validate_workspace_name,
)

__all__ = [
    # Helper functions
    "setup_logging",
    "chunk_list",
    "format_phone_for_display",
    "calculate_message_cost",
    "get_current_timestamp",
    "parse_iso_timestamp",
    "safe_json_extract",
    "run_async",
    "mask_sensitive_data",
    "build_user_agent",
    # Validation functions
    "validate_phone_number",
    "normalize_phone_number",
    "validate_phone_numbers",
    "validate_sender_id",
    "validate_message_content",
    "validate_workspace_name",
    "validate_campaign_name",
    "validate_uuid",
]
