"""Custom exceptions for the Briq SDK."""

from typing import Any, Dict, Optional


class BriqError(Exception):
    """Base exception for all Briq SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize BriqError.

        Args:
            message: Error message.
            status_code: HTTP status code if applicable.
            response_data: Response data from the API if available.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class BriqAPIError(BriqError):
    """Exception raised for API errors from the Briq service."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ) -> None:
        """Initialize BriqAPIError.

        Args:
            message: Error message from the API.
            status_code: HTTP status code.
            response_data: Full response data from the API.
            error_code: Specific error code from the API.
        """
        super().__init__(message, status_code, response_data)
        self.error_code = error_code


class BriqAuthenticationError(BriqAPIError):
    """Exception raised for authentication errors (401)."""

    def __init__(
        self,
        message: str = "Invalid API key or authentication failed",
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, 401, response_data, "AUTHENTICATION_ERROR")


class BriqAuthorizationError(BriqAPIError):
    """Exception raised for authorization errors (403)."""

    def __init__(
        self,
        message: str = "Insufficient permissions for this operation",
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, 403, response_data, "AUTHORIZATION_ERROR")


class BriqNotFoundError(BriqAPIError):
    """Exception raised when a resource is not found (404)."""

    def __init__(
        self,
        message: str = "The requested resource was not found",
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, 404, response_data, "NOT_FOUND_ERROR")


class BriqValidationError(BriqAPIError):
    """Exception raised for validation errors (400, 422)."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        response_data: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize BriqValidationError.

        Args:
            message: Error message.
            status_code: HTTP status code (400 or 422).
            response_data: Response data from the API.
            validation_errors: Detailed validation errors by field.
        """
        super().__init__(message, status_code, response_data, "VALIDATION_ERROR")
        self.validation_errors = validation_errors or {}


class BriqRateLimitError(BriqAPIError):
    """Exception raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        response_data: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        """Initialize BriqRateLimitError.

        Args:
            message: Error message.
            response_data: Response data from the API.
            retry_after: Number of seconds to wait before retrying.
        """
        super().__init__(message, 429, response_data, "RATE_LIMIT_ERROR")
        self.retry_after = retry_after


class BriqServerError(BriqAPIError):
    """Exception raised for server errors (5xx)."""

    def __init__(
        self,
        message: str = "Internal server error",
        status_code: int = 500,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, response_data, "SERVER_ERROR")


class BriqNetworkError(BriqError):
    """Exception raised for network-related errors."""

    def __init__(
        self,
        message: str = "Network error occurred",
        original_error: Optional[Exception] = None,
    ) -> None:
        """Initialize BriqNetworkError.

        Args:
            message: Error message.
            original_error: The original exception that caused this error.
        """
        super().__init__(message)
        self.original_error = original_error


class BriqTimeoutError(BriqNetworkError):
    """Exception raised when a request times out."""

    def __init__(
        self,
        message: str = "Request timeout",
        timeout_duration: Optional[float] = None,
    ) -> None:
        """Initialize BriqTimeoutError.

        Args:
            message: Error message.
            timeout_duration: The timeout duration that was exceeded.
        """
        super().__init__(message)
        self.timeout_duration = timeout_duration


def create_api_error(
    status_code: int,
    message: str,
    response_data: Optional[Dict[str, Any]] = None,
    error_code: Optional[str] = None,
) -> BriqAPIError:
    """Factory function to create appropriate API error based on status code.

    Args:
        status_code: HTTP status code.
        message: Error message.
        response_data: Response data from the API.
        error_code: Specific error code from the API.

    Returns:
        Appropriate BriqAPIError subclass instance.
    """
    if status_code == 401:
        return BriqAuthenticationError(message, response_data)
    elif status_code == 403:
        return BriqAuthorizationError(message, response_data)
    elif status_code == 404:
        return BriqNotFoundError(message, response_data)
    elif status_code in (400, 422):
        validation_errors = None
        if response_data and "errors" in response_data:
            validation_errors = response_data["errors"]
        return BriqValidationError(
            message, status_code, response_data, validation_errors
        )
    elif status_code == 429:
        retry_after = None
        if response_data and "retry_after" in response_data:
            retry_after = response_data["retry_after"]
        return BriqRateLimitError(message, response_data, retry_after)
    elif status_code >= 500:
        return BriqServerError(message, status_code, response_data)
    else:
        return BriqAPIError(message, status_code, response_data, error_code)
