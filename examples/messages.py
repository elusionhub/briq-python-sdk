from elusion.briq import Briq
from elusion.briq.models.message import InstantMessage
import asyncio


async def test_connection():
    async with Briq() as client:
        try:
            print(await client.test_connection())
        except Exception as e:
            print(f"Failed to connect to Briq API: {e}")


async def sendMessage():
    async with Briq() as client:
        message_data = InstantMessage(
            recipients=["0781588379"],
            content="Hello, this is a test message!",
            sender_id="BRIQ",
        )

        try:
            response = await client.messages.send_instant(message_data)
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to send message: {e}")


async def getMessageLogs():
    async with Briq() as client:
        try:
            logs = await client.messages.get_logs()
            print(logs.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to retrieve message logs: {e}")


async def getMessageHistory():
    async with Briq() as client:
        try:
            history = await client.messages.get_history()
            print(history.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to retrieve message history: {e}")


if __name__ == "__main__":
    # asyncio.run(test_connection())
    # asyncio.run(sendMessage())
    asyncio.run(getMessageLogs())
    # asyncio.run(getMessageHistory())
