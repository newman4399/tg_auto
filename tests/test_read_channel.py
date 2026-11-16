import asyncio
from telethon import TelegramClient

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    CHECKIN_TEXT,
    CHECKIN_HOUR,
    CHECKIN_MINUTE,
    TIMEZONE,
)
API_ID = TELEGRAM_API_ID
API_HASH = TELEGRAM_API_HASH

async def main():
    client = TelegramClient(
        "telegram_checkin",
        API_ID,
        API_HASH
    )

    await client.start()

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            print(
                "群组名称:", dialog.name,
                "群组 ID:", dialog.id
            )

    await client.disconnect()

asyncio.run(main())