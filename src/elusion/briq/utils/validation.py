"""Validation utilities for the Briq SDK."""

import re
from typing import List


def validate_phone_number(phone: str) -> bool:
    """Validate a phone number format.

    Args:
        phone: Phone number to validate.

    Returns:
        True if the phone number is valid, False otherwise.

    Examples:
        >>> validate_phone_number("2557000000000")
        True
        >>> validate_phone_number("+2557000000000")
        True
        >>> validate_phone_number("invalid")
        False
    """
    if not phone:
        return False

    # Remove non-digit characters except +
    cleaned = re.sub(r"[^\d+]", "", phone)

    # Must start with + or digit, and be at least 10 digits
    if not re.match(r"^(\+)?[1-9]\d{9,}$", cleaned):
        return False

    # Remove + for length check
    digits_only = cleaned.lstrip("+")

    # Must be between 10 and 15 digits (E.164 standard)
    return 10 <= len(digits_only) <= 15


def normalize_phone_number(phone: str) -> str:
    """Normalize a phone number to a standard format.

    Args:
        phone: Phone number to normalize.

    Returns:
        Normalized phone number.

    Examples:
        >>> normalize_phone_number("+255 781 588 379")
        "2557000000000"
        >>> normalize_phone_number("(255) 781-588-379")
        "2557000000000"
    """
    if not phone:
        return ""

    # Remove all non-digit characters except +
    cleaned = re.sub(r"[^\d+]", "", phone)

    # Remove leading + if present
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    return cleaned


def validate_phone_numbers(phones: List[str]) -> List[str]:
    """Validate and normalize a list of phone numbers.

    Args:
        phones: List of phone numbers to validate.

    Returns:
        List of valid, normalized phone numbers.

    Raises:
        ValueError: If any phone number is invalid.

    Examples:
        >>> validate_phone_numbers(["+2557000000000", "255781588380"])
        ["2557000000000", "255781588380"]
    """
    if not phones:
        raise ValueError("At least one phone number is required")

    validated_phones: List[str] = []
    for phone in phones:
        normalized = normalize_phone_number(phone)
        if not validate_phone_number(normalized):
            raise ValueError(f"Invalid phone number: {phone}")
        validated_phones.append(normalized)

    return validated_phones


def validate_sender_id(sender_id: str) -> str:
    """Validate and normalize a sender ID.

    Args:
        sender_id: Sender ID to validate.

    Returns:
        Normalized sender ID.

    Raises:
        ValueError: If sender ID is invalid.

    Examples:
        >>> validate_sender_id("BRIQ")
        "BRIQ"
        >>> validate_sender_id("My Company!")
        "MYCOMPANY"
    """
    if not sender_id:
        raise ValueError("Sender ID cannot be empty")

    # Remove non-alphanumeric characters and convert to uppercase
    normalized = re.sub(r"[^A-Za-z0-9]", "", sender_id).upper()

    if not normalized:
        raise ValueError("Sender ID must contain at least one alphanumeric character")

    if len(normalized) > 11:
        normalized = normalized[:11]

    return normalized


def validate_message_content(content: str, max_length: int = 1600) -> str:
    """Validate message content.

    Args:
        content: Message content to validate.
        max_length: Maximum allowed length.

    Returns:
        Validated message content.

    Raises:
        ValueError: If content is invalid.

    Examples:
        >>> validate_message_content("Hello world!")
        "Hello world!"
        >>> validate_message_content("")
        ValueError: Message content cannot be empty
    """
    if not content:
        raise ValueError("Message content cannot be empty")

    content = content.strip()
    if not content:
        raise ValueError("Message content cannot be empty or whitespace only")

    if len(content) > max_length:
        raise ValueError(f"Message content cannot exceed {max_length} characters")

    return content


def validate_workspace_name(name: str) -> str:
    """Validate workspace name.

    Args:
        name: Workspace name to validate.

    Returns:
        Validated workspace name.

    Raises:
        ValueError: If name is invalid.

    Examples:
        >>> validate_workspace_name("My Project")
        "My Project"
        >>> validate_workspace_name("   ")
        ValueError: Workspace name cannot be empty
    """
    if not name:
        raise ValueError("Workspace name cannot be empty")

    name = name.strip()
    if not name:
        raise ValueError("Workspace name cannot be empty or whitespace only")

    if len(name) > 255:
        raise ValueError("Workspace name cannot exceed 255 characters")

    return name


def validate_campaign_name(name: str) -> str:
    """Validate campaign name.

    Args:
        name: Campaign name to validate.

    Returns:
        Validated campaign name.

    Raises:
        ValueError: If name is invalid.

    Examples:
        >>> validate_campaign_name("Summer Sale")
        "Summer Sale"
        >>> validate_campaign_name("")
        ValueError: Campaign name cannot be empty
    """
    if not name:
        raise ValueError("Campaign name cannot be empty")

    name = name.strip()
    if not name:
        raise ValueError("Campaign name cannot be empty or whitespace only")

    if len(name) > 255:
        raise ValueError("Campaign name cannot exceed 255 characters")

    return name


def validate_uuid(uuid_string: str, field_name: str = "ID") -> str:
    """Validate a UUID string.

    Args:
        uuid_string: UUID string to validate.
        field_name: Name of the field for error messages.

    Returns:
        Validated UUID string.

    Raises:
        ValueError: If UUID is invalid.

    Examples:
        >>> validate_uuid("466e6a77-6f38-4b51-afbb-4b63ebf4ff43")
        "466e6a77-6f38-4b51-afbb-4b63ebf4ff43"
        >>> validate_uuid("invalid")
        ValueError: Invalid ID format
    """
    if not uuid_string:
        raise ValueError(f"{field_name} cannot be empty")

    # Basic UUID format validation (8-4-4-4-12 hex digits)
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

    if not re.match(uuid_pattern, uuid_string.lower()):
        raise ValueError(f"Invalid {field_name} format")

    return uuid_string.lower()
