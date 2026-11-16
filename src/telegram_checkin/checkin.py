import asyncio
import logging
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient
from telethon.errors import FloodError, RPCError
from telethon.tl.types import Channel, Chat

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    CHECKIN_TEXT,
    CHECKIN_HOUR,
    CHECKIN_MINUTE,
    TIMEZONE,
)

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
    "telegram_checkin",
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

# ===============
# 主程序
# ===============

async def main():
    logger.info("正在连接 TG")

    await client.start()

    me = await client.get_me()

    # 先启动时打印一次当前群组
    logger.info("当前可访问的目标群组:")

    count = 0

    async for dialog in client.iter_dialogs():

        if is_target_group(dialog.entity):

            count += 1

            logger.info(
                "  [%s] %s",
                count,
                dialog.name,
            )

    logger.info(
        "共发现 %s 个普通群/超级群",
        count,
    )

    # ================
    # 定时器
    # ================

    schedule = AsyncIOScheduler(
        timezone=TIMEZONE
    )

    schedule.add_job(
        do_checkin,
        trigger="cron",
        hour=CHECKIN_HOUR,
        minute=CHECKIN_MINUTE,
        id="daily_checkin",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    schedule.start()

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序已停止")