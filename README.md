# Briq Python SDK

A modern Python SDK for the Briq SMS API with full async/await support and comprehensive type safety.

## Installation

```bash
pip install briq-sdk
# or
poetry add briq-sdk
```

## Quick Start

```python
import asyncio
from briq import Briq

async def main():
    async with Briq(api_key="your-api-key") as client:
        # Send an instant message
        response = await client.messages.send_instant({
            "recipients": ["255700000000"],
            "content": "Hello from Briq!",
            "sender_id": "your-sender-id"
        })
        print(f"Message sent: {response.data.status}")

asyncio.run(main())
```

## Features

- **Modern Async/Await** - Full asyncio support with sync fallback
- **Type Safety** - Complete type hints with Pydantic validation
- **Instant Messages** - Send SMS to single or multiple recipients
- **Campaign Management** - Create and manage SMS campaigns
- **Workspace Organization** - Organize projects and teams
- **Message Tracking** - Real-time delivery status and logs
- **High Performance** - Built on httpx and asyncio
- **Error Handling** - Comprehensive exception hierarchy

## Core Services

### Messages

```python
# Send instant message
async with Briq() as client:
    await client.messages.send_instant({
        "recipients": ["255781588379", "255781588380"],
        "content": "Your message here",
        "sender_id": "BRIQ"
    })

    # Get message logs
    logs = await client.messages.get_logs()

    # Check message status
    status = await client.messages.get_status("message-id")
```

### Campaigns

```python
# Create campaign
async with Briq() as client:
    campaign = await client.campaigns.create({
        "name": "Summer Sale",
        "description": "Promotional campaign",
        "workspace_id": "workspace-id",
        "launch_date": "2025-07-01T10:00:00Z"
    })

    # Send campaign message
    await client.messages.send_campaign({
        "campaign_id": campaign.data.id,
        "group_id": "group-id",
        "content": "Special offer inside!",
        "sender_id": "BRIQ"
    })
```

### Workspaces

```python
# Create workspace
async with Briq() as client:
    workspace = await client.workspaces.create({
        "name": "My Project",
        "description": "SMS campaigns for my project"
    })

    # List all workspaces
    workspaces = await client.workspaces.list()
```

## Configuration

```python
from briq import Briq

# Basic initialization
client = Briq(api_key="your-api-key")

# Advanced configuration
client = Briq(
    api_key="your-api-key",
    base_url="https://karibu.briq.tz",  # optional
    timeout=30.0,  # optional, default 30s
    max_retries=3,  # optional, default 3
    headers={  # optional custom headers
        "X-Custom-Header": "value"
    }
)
```

## Async vs Sync Usage

### Async (Recommended)

```python
import asyncio
from briq import Briq

async def main():
    async with Briq() as client:
        response = await client.messages.send_instant({
            "recipients": ["255781588379"],
            "content": "Async message",
            "sender_id": "BRIQ"
        })
        print(f"Status: {response.data.status}")

asyncio.run(main())
```

### Sync (Alternative)

```python
from briq import Briq

with Briq() as client:
    response = client.messages.send_instant_sync({
        "recipients": ["255700000000"],
        "content": "Sync message",
        "sender_id": "your-sender-id"
    })
    print(f"Status: {response.data.status}")
```

## Error Handling

```python
from briq import Briq, BriqAPIError, BriqRateLimitError

async with Briq() as client:
    try:
        await client.messages.send_instant({
            "recipients": ["invalid-number"],
            "content": "Test message",
            "sender_id": "your-sender-id"
        })
    except BriqRateLimitError as e:
        print(f"Rate limited: {e.retry_after} seconds")
    except BriqAPIError as e:
        print(f"API error {e.status_code}: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Environment Variables

```bash
# Set your API key
export BRIQ_API_KEY=your-api-key-here

# Optional: Custom API base URL
export BRIQ_BASE_URL=https://karibu.briq.tz
```

## Type Safety

The SDK provides full type hints and runtime validation:

```python
from elusion.briq.models import InstantMessage, Workspace

# Type-safe message creation
message_data = InstantMessage(
    recipients=["255700000000"],
    content="Type-safe message",
    sender_id="your-sender-id"
)

# Pydantic validation ensures data integrity
async with Briq() as client:
    response = await client.messages.send_instant(message_data)
    workspace: Workspace = response.data  # Fully typed response
```

## Advanced Features

### Bulk Operations

```python
# Send to multiple recipients efficiently
recipients = ["255700000000", "255700000000", "255700000000"]

async with Briq() as client:
    response = await client.messages.send_instant({
        "recipients": recipients,
        "content": "Bulk message",
        "sender_id": "BRIQ"
    })

    # Handle individual results
    for msg in response.data:
        print(f"{msg.recipient}: {msg.status}")
```

### Message History with Filtering

```python
from datetime import datetime, timedelta

async with Briq() as client:
    # Get delivered messages from last week
    history = await client.messages.get_history({
        "status": "delivered",
        "limit": 100
    })
```

### Campaign Management

```python
async with Briq() as client:
    # Create and manage campaign lifecycle
    campaign = await client.campaigns.create({...})

    # Control campaign status
    await client.campaigns.pause(campaign.data.id)
    await client.campaigns.resume(campaign.data.id)
    await client.campaigns.cancel(campaign.data.id)
```

## Development

```bash
# Clone and install
git clone https://github.com/elusionhub/briq-python-sdk.git
cd briq-python-sdk
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/briq

# Format code
black src/ tests/
ruff src/ tests/

# Type checking
mypy src/
```

## Requirements

- Python 3.8+
- httpx >= 0.25.0
- pydantic >= 2.0.0

## License

MIT © [Elution Hub](https://github.com/elusionhub)

## Support

- Email: elusion.lab@gmail.com
- Issues: [GitHub Issues](https://github.com/elusionhub/briq-python-sdk/issues)
- Docs: [API Documentation](https://github.com/elusionhub/briq-python-sdk#readme)
