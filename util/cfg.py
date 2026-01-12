import os
import discord
from dotenv import load_dotenv

__all__ = ["log_level", "save_log", "bot", "whitelist"]

env = load_dotenv(os.path.join(os.getcwd(), ".env"))

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
    print(
        "❌ LOG LEVEL IN CONFIG FILE NOT VALID. PLEASE USE ON OF THE OPTIONS SUPPLIED IN THE TEMPLATE. DEFAULTING TO 'INFO' ❌"
    )
    log_level = "INFO"

save_log = os.getenv("SAVE_LOG", "0").lower() in ("true", "1", "t", "y")


class bot:
    token = os.getenv("BOT_TOKEN")
    name = os.getenv("BOT_NAME", "BotBouncer")
    guild_id = int(os.getenv("BOT_GUILD_ID", "0"))
    accent_color = discord.Color.from_str("#" + os.getenv("BOT_ACCENTCOLOR", "eba4be"))


class image:
    unknown = "https://imgur.com/a/jql8DP5"
    boombox = "https://imgur.com/a/33ed4oY"
