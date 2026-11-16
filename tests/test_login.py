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
        API_HASH,
        use_ipv6=False
    )

    try:
        await client.start()

        me = await client.get_me()

        print("登录成功！")
        print("用户 ID:", me.id)
        print("用户名:", me.username)
        print("姓名:", me.first_name)

    finally:
        await client.disconnect()

asyncio.run(main())