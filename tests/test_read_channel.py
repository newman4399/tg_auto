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

def strip_name(name: str):
    import re
    # 循环消除嵌套 ()，正则递归匹配括号内容
    pattern = r"\([^()]*\)"
    while re.search(pattern, s):
        s = re.sub(pattern, "", s)
    # 只保留中文、大小写英文字母
    s = re.sub(r"[^\u4e00-\u9fa5a-zA-Z]", "", s)
    return s

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
                "群组名称:", strip_name(dialog.name),
                "群组 ID:", dialog.id
            )

    await client.disconnect()

asyncio.run(main())