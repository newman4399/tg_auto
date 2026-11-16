import os
import asyncio
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from checkin import client, is_target_group, do_routine
from config import (
    TIMEZONE,
    CHECKIN_HOUR,
    CHECKIN_MINUTE
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("tg-main")


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
        do_routine,
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
