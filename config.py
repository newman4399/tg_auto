import os

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API_ID = int(os.environ["TELEGRAM_API_ID"])
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]

CHECKIN_TEXT = os.getenv("CHECKIN_TEXT", "签到")

CHECKIN_HOUR = int(os.getenv("CHECKIN_HOUR", "12"))
CHECKIN_MINUTE = int(os.getenv("CHECKIN_MINUTE", "0"))

TIMEZONE = os.getenv("TIMEZONE", "Asia/Shanghai")