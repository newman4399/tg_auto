import asyncio
import logging
import os
from datetime import datetime


from telethon import TelegramClient
from telethon.errors import FloodError, RPCError
from telethon.tl.types import Channel, Chat

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    CHECKIN_TEXT
)

API_ID = TELEGRAM_API_ID
API_HASH = TELEGRAM_API_HASH
# =============
# 日志
# =============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("tg-checkin")

# =========================
# Session
# =========================

SESSION_DIR = "sessions"
SESSION_NAME = os.path.join(
    SESSION_DIR,
    "telegram_checkin.session",
)

os.makedirs(SESSION_DIR, exist_ok=True)

client = TelegramClient(
    SESSION_NAME,
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
)

# =========================
# 判断是否为普通群 / 超级群
# =========================
def is_target_group(entity) -> bool:
    """
    只允许普通群和超级群
    chat
    channel
    """

    if isinstance(entity, Chat):
        return True

    if isinstance(entity, Channel):
        return bool(getattr(entity, "megagroup", False))

    return False

# ==========
# 执行签到
# ==========

async def do_checkin():
    logger.info("=" * 60)
    logger.info("开始每日签到")
    logger.info("签到内容： %s", CHECKIN_TEXT)

    success = 0
    failed = 0
    skipped = 0

    async for dialog in client.iter_dialogs():

        entity = dialog.entity

        if not (is_target_group(entity)):
            continue

        group_name = dialog.name or "无名称"

        try:
            logger.info(
                "正在签到：%s",
                group_name
            )

            await client.send_message(entity, CHECKIN_TEXT)

            success += 1

            logger.info(
                "签到成功: %s",
                group_name,
            )
            # 稍微停一下，避免短时间向大量群发送消息
            await asyncio.sleep(1)

        except FloodError as e:
            logger.warning(
                "TG要求等待 %s 秒， 群组： %s",
                e.seconds,
                group_name,
            )

            failed += 1

            continue
        except RPCError as e:

            failed += 1

            logger.error(
                "Telegram API 错误 | 群组=%s | error=%s",
                group_name,
                e,
            )

        except Exception as e:

            failed += 1

            logger.exception(
                "未知错误 | 群组=%s | error=%s",
                group_name,
                e,
            )

        logger.info(
            "签到完成 | 成功=%s | 失败=%s | 跳过=%s",
            success,
            failed,
            skipped,
        )

        logger.info("=" * 60)

def default_waffle_string(group_name: str, repeat_n=5)->list:
    return [group_name+str(n) for n in range(1, repeat_n)]

def strip_name(s: str):
    import re
    # 循环消除嵌套 ()，正则递归匹配括号内容
    pattern = r"\([^()]*\)"
    while re.search(pattern, s):
        s = re.sub(pattern, "", s)
    # 只保留中文、大小写英文字母
    s = re.sub(r"[^\u4e00-\u9fa5a-zA-Z]", "", s)
    return s

waffes = {"-1001330784088":True, "-1003958359489":True}

async def do_waffle(waffes: dict, repeat_n: int = 10):
    # waffes: {"group_id": bool / string/ func}
    logger.info("=" * 60)
    logger.info("开始每日水群")

    success = 0
    failed = 0
    skipped = 0

    async for dialog in client.iter_dialogs():

        entity = dialog.entity

        if not (is_target_group(entity)):
            continue

        group_name = dialog.name or "无名称"

        try:

            msgs = []
            group_waffle = waffes.get(str(dialog.id), None)
            if group_waffle == False:
                # 不向false群组发送消息
                continue
            elif group_waffle is not None:
                # 默认消息
                logger.info(
                "正在水群：%s",
                group_name
            )
                msgs += "每天晚上按时在群里发言"
                msgs += "给群里增加活跃度"
                msgs += "给自己攒一点积分"
                msgs += default_waffle_string(group_name)
            else:
                # 特定群组消息
                continue
                msgs += "每天晚上按时在群里发言"
                msgs += "给群里增加活跃度"
                msgs += "给自己攒一点积分"
                msgs = [group_waffle] + default_waffle_string(group_name)

            for n in range(len(msgs)):
                await client.send_message(entity, msgs[n])
                await asyncio.sleep(1)
            

            success += 1

            logger.info(
                "水群成功: %s",
                group_name,
            )
            # 稍微停一下，避免短时间向大量群发送消息
            await asyncio.sleep(2)

        except FloodError as e:
            logger.warning(
                "TG要求等待 %s 秒， 群组： %s",
                e.seconds,
                group_name,
            )

            failed += 1

            continue
        except RPCError as e:

            failed += 1

            logger.error(
                "Telegram API 错误 | 群组=%s | error=%s",
                group_name,
                e,
            )

        except Exception as e:

            failed += 1

            logger.exception(
                "未知错误 | 群组=%s | error=%s",
                group_name,
                e,
            )

        logger.info(
            "水群完成 | 成功=%s | 失败=%s | 跳过=%s",
            success,
            failed,
            skipped,
        )

        logger.info("=" * 60)



async def do_routine():
    await do_checkin()
    await do_waffle(waffes)


async def main():
    await client.start()

    # await do_checkin()
    await do_waffle(waffes)

if __name__ == "__main__":
    asyncio.run(main())