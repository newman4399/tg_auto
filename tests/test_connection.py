import asyncio
import logging
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
logging.basicConfig(level=logging.DEBUG)



async def main():
    client = TelegramClient(
        "test_session",
        API_ID,
        API_HASH,
        timeout=15,
        connection_retries=2,
        retry_delay=2,
        use_ipv6=False
    )

    try:
        print("正在连接 Telegram...")
        await client.connect()

        print("连接状态:", client.is_connected())

        if await client.is_user_authorized():
            me = await client.get_me()
            print("登录成功:", me.first_name)
        else:
            print("网络已连接，但尚未登录")
    except Exception as e:
        print("错误类型:", type(e).__name__)
        print("错误内容:", repr(e))
    finally:
        await client.disconnect()

asyncio.run(main())