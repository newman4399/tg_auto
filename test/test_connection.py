import asyncio
import logging
from telethon import TelegramClient

logging.basicConfig(level=logging.DEBUG)

API_ID = 你的_api_id
API_HASH = "你的_api_hash"

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