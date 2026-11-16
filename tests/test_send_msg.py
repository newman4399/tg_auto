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

TARGET_GROUP_ID = -1001778319982

async def main():
    client = TelegramClient(
        "telegram_checkin",
        API_ID,
        API_HASH,
        use_ipv6=False
    )

    try:
        await client.start()
        target = None
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                if dialog.id == TARGET_GROUP_ID:
                    target = dialog.entity
                    print("找到测试群组：", dialog.name)
                    break

        if target is None:
            print("没有找到测试群组")
            return

        await client.send_message(target, "签到")
        print("签到成功")


    finally:
        await client.disconnect()

asyncio.run(main())