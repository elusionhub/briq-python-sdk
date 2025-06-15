"""Message service for the Briq SDK."""

from typing import Dict, List, Union

from elusion.briq.models.common import APIResponse
from elusion.briq.models.message import (
    CampaignMessage,
    InstantMessage,
    Message,
    MessageHistory,
    MessageListParams,
    MessageLog,
    MessageLogParams,
    MessageStatus,
    MessageResponse,
)
from elusion.briq.services.base import BaseService


class MessageService(BaseService):
    """Service for sending and managing messages."""

    # Async methods
    async def send_instant(
        self,
        message_data: Union[InstantMessage, Dict[str, Union[str, List[str]]]],
    ) -> APIResponse[Union[Message, List[Message]]]:
        """Send instant messages to recipients.

        Args:
            message_data: Instant message data including recipients, content, and sender_id.

        Returns:
            Sent message(s). Returns a single Message for one recipient,
            or a list of Messages for multiple recipients.

        Examples:
            >>> # Send to single recipient
            >>> async with briq_client:
            ...     response = await briq_client.messages.send_instant({
            ...         "recipients": ["255781588379"],
            ...         "content": "Hello from Briq!",
            ...         "sender_id": "sender_id"
            ...     })
            ...     print(f"Message sent: {response.data.status}")

            >>> # Send to multiple recipients
            >>> async with briq_client:
            ...     response = await briq_client.messages.send_instant({
            ...         "recipients": ["255781588379", "255781588380"],
            ...         "content": "Bulk message",
            ...         "sender_id": "sender_id"
            ...     })
            ...     for msg in response.data:
            ...         print(f"To {msg.recipient}: {msg.status}")
        """
        url = self._build_url("messages-instant")
        serialized_data = self._validate_and_serialize(message_data)

        response_data = await self.http_client.post(url, data=serialized_data)

        return self._parse_response(response_data, MessageResponse)

    async def send_campaign(
        self, message_data: Union[CampaignMessage, Dict[str, str]]
    ) -> APIResponse[Dict[str, Union[str, int]]]:
        """Send a message via campaign.

        Args:
            message_data: Campaign message data including campaign_id, content, and sender_id.

        Returns:
            Campaign message sending result with statistics.

        Examples:
            >>> async with briq_client:
            ...     response = await briq_client.messages.send_campaign({
            ...         "campaign_id": "campaign-123",
            ...         "group_id": "group-456",
            ...         "content": "Campaign message content",
            ...         "sender_id": "sender_id"
            ...     })
            ...     print(f"Messages sent: {response.data['messages_sent']}")
        """
        url = self._build_url("messages-campaign")
        serialized_data = self._validate_and_serialize(message_data)

        response_data = await self.http_client.post(url, data=serialized_data)
        return APIResponse[Dict[str, Union[str, int]]](
            success=response_data.get("success", True),
            data=response_data,
            message=response_data.get("message"),
            error=response_data.get("error"),
        )

    async def get_history(
        self, params: Union[MessageListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[MessageHistory]]:
        """Get message history.

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of messages with history.

        Examples:
            >>> async with briq_client:
            ...     messages = await briq_client.messages.get_history({
            ...         "status": "delivered",
            ...         "limit": 100
            ...     })
            ...     for msg in messages.data:
            ...         print(f"{msg.recipient}: {msg.status}")
        """
        if isinstance(params, dict):
            params = MessageListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return await self._list("messages-history", MessageHistory, params)

    async def get_logs(
        self, params: Union[MessageLogParams, Dict[str, str], None] = None
    ) -> APIResponse[MessageLog]:
        """Get message logs for tracking delivery status.

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of message logs.

        Examples:
            >>> async with briq_client:
            ...     logs = await briq_client.messages.get_logs({
            ...         "message_id": "msg-123",
            ...         "status": "delivered"
            ...     })
            ...     for log in logs.data:
            ...         print(f"Log: {log.status} at {log.timestamp}")
        """
        if isinstance(params, dict):
            params = MessageLogParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return await self._get("messages-logs", MessageLog)

    async def get_status(self, message_id: str) -> APIResponse[MessageStatus]:
        """Get the current status of a specific message.

        Args:
            message_id: The message ID to check status for.

        Returns:
            Current message status.

        Examples:
            >>> async with briq_client:
            ...     status = await briq_client.messages.get_status("msg-123")
            ...     print(f"Status: {status.data.status}")
            ...     if status.data.delivered_at:
            ...         print(f"Delivered at: {status.data.delivered_at}")
        """
        url = self._build_url("messages", f"{message_id}/status")
        response_data = await self.http_client.get(url)
        return self._parse_response(response_data, MessageStatus)

    async def cancel(self, message_id: str) -> APIResponse[MessageStatus]:
        """Cancel a pending message.

        Args:
            message_id: The message ID to cancel.

        Returns:
            Updated message status.

        Examples:
            >>> async with briq_client:
            ...     cancelled = await briq_client.messages.cancel("msg-123")
            ...     print(f"Message cancelled: {cancelled.data.status}")
        """
        url = self._build_url("messages", f"{message_id}/cancel")
        response_data = await self.http_client.post(url)
        return self._parse_response(response_data, MessageStatus)

    # Sync methods
    def send_instant_sync(
        self,
        message_data: Union[InstantMessage, Dict[str, Union[str, List[str]]]],
    ) -> APIResponse[Union[Message, List[Message]]]:
        """Send instant messages to recipients (sync version).

        Args:
            message_data: Instant message data including recipients, content, and sender_id.

        Returns:
            Sent message(s).
        """
        url = self._build_url("messages_instant")
        serialized_data = self._validate_and_serialize(message_data)

        response_data = self.http_client.post_sync(url, data=serialized_data)

        # Handle both single message and bulk message responses
        if isinstance(response_data.get("data"), list):
            return self._parse_response(response_data, Message, is_list=True)
        else:
            return self._parse_response(response_data, Message)

    def send_campaign_sync(
        self, message_data: Union[CampaignMessage, Dict[str, str]]
    ) -> APIResponse[Dict[str, Union[str, int]]]:
        """Send a message via campaign (sync version).

        Args:
            message_data: Campaign message data.

        Returns:
            Campaign message sending result.
        """
        url = self._build_url("messages_campaign")
        serialized_data = self._validate_and_serialize(message_data)

        response_data = self.http_client.post_sync(url, data=serialized_data)
        return APIResponse[Dict[str, Union[str, int]]](
            success=response_data.get("success", True),
            data=response_data.get("data", {}),
            message=response_data.get("message"),
            error=response_data.get("error"),
        )

    def get_history_sync(
        self, params: Union[MessageListParams, Dict[str, str], None] = None
    ) -> APIResponse[List[Message]]:
        """Get message history (sync version).

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of messages with history.
        """
        if isinstance(params, dict):
            params = MessageListParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return self._list_sync("messages_history", Message, params)

    def get_logs_sync(
        self, params: Union[MessageLogParams, Dict[str, str], None] = None
    ) -> APIResponse[List[MessageLog]]:
        """Get message logs (sync version).

        Args:
            params: Optional filtering and pagination parameters.

        Returns:
            List of message logs.
        """
        if isinstance(params, dict):
            params = MessageLogParams(
                **params,
                page=int(params.get("page", 1)) if params else 1,
                limit=int(params.get("limit", 10)) if params else 10,
            )
        return self._list_sync("messages_logs", MessageLog, params)

    def get_status_sync(self, message_id: str) -> APIResponse[MessageStatus]:
        """Get message status (sync version).

        Args:
            message_id: The message ID to check status for.

        Returns:
            Current message status.
        """
        url = self._build_url("messages", f"{message_id}/status")
        response_data = self.http_client.get_sync(url)
        return self._parse_response(response_data, MessageStatus)

    def cancel_sync(self, message_id: str) -> APIResponse[MessageStatus]:
        """Cancel a pending message (sync version).

        Args:
            message_id: The message ID to cancel.

        Returns:
            Updated message status.
        """
        url = self._build_url("messages", f"{message_id}/cancel")
        response_data = self.http_client.post_sync(url)
        return self._parse_response(response_data, MessageStatus)
