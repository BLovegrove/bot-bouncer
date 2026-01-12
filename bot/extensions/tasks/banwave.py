import datetime as dt
import json
import os
import zoneinfo
import discord
from discord.ext import tasks, commands
from loguru import logger

from util import models, cfg
from util.handlers.banlog import BanLogHandler


class BanWave(commands.Cog):
    def __init__(self, bot: models.BouncerBot):
        self.task.start()
        self.bot = bot
        self.banlog = BanLogHandler()

    @tasks.loop(time=dt.time(hour=0, minute=0, second=0))
    async def task(self):
        await self.execute_ban()

    async def execute_ban(self, itr: discord.Interaction = None):
        guild = self.bot.get_guild(cfg.bot.guild_id)
        reply_channel = guild.system_channel

        if not reply_channel:
            logger.error(
                "Oops! No system channel found for banwave task. You might have configured something wrong."
            )
            return

        if not os.path.exists("whitelist.json"):
            logger.warning(
                "No whitelist detected. If you want to ban *all* bots, create the file with an empty list. Either way, a file *is* required."
            )
            return

        whitelist = []
        with open("whitelist.json", "r") as file:
            whitelist = json.load(file)
            file.close()

        all_members = guild.members
        to_ban: list[discord.Member] = []
        for member in all_members:
            if member.bot and member.id not in whitelist:
                to_ban.append(member)

        message = "Cheeky cockroach detected - laugh at discord for their failure to get past the Bouncer :face_with_hand_over_mouth:\n\n"

        for bot in to_ban:
            message + f"- {bot.name}\n"

            ban_count = self.banlog[bot.id]["ban_count"]
            ban_data = {
                "name": bot.name,
                "ban_count": 0 if not ban_count else (ban_count + 1),
                "ban_status": False,
            }
            self.banlog.add_entry(bot.id, ban_data)
            self.banlog.save_data()

            bot.ban(bot, 99999)

            ban_data["ban_status"] = True
            self.banlog.add_entry(bot.id, ban_data)
            self.banlog.save_data()

        await reply_channel.send(content=message)
        logger.info(f"Discord bots detected and eliminated: {to_ban}")


async def setup(bot):
    await bot.add_cog(BanWave(bot))
