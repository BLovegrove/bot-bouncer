# core imports
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from loguru import logger

# custom imports
from util import cfg, models
from bot.extensions.tasks import banwave


class Admin(commands.Cog):
    def __init__(self, bot: models.BouncerBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="admin",
        description=f"Runs a series of dev commands for testing and maintenance purposes.",
    )
    @app_commands.choices(
        command=[
            Choice(name="Kill bot", value="die"),
            Choice(name="Ping test", value="ping"),
            Choice(name="Ban wave test", value="banwave"),
            Choice(name="List all member IDs", value="list_ids"),
        ]
    )
    @commands.is_owner()
    async def admin(self, itr: discord.Interaction, command: Choice[str]):
        match command.value:
            case "die":
                await itr.response.send_message(
                    f"Restarting the bot. Please wait until {cfg.bot.name} has the 'Online' or 'Idle' status icon before doing any more commands.",
                    ephemeral=True,
                )
                # self.bot.tree.clear_commands(guild=itr.guild)
                # await self.bot.tree.sync(guild=itr.guild)
                # logger.info(f"Cleared all commands.")

                await self.bot.change_presence(status=discord.Status.offline)
                await self.bot.close()
                return

            case "ping":
                await itr.response.send_message(
                    f"Pong! Here are the round trip times: \n"
                    + f"Bot: {round(self.bot.latency * 1000)}ms",
                    ephemeral=True,
                )
                return

            case "banwave":
                bw_test = banwave.BanWave(self.bot)
                await bw_test.execute_ban()
                return

            case "list_ids":
                await itr.response.defer()
                members = itr.guild.members
                friendly_list = []

                for member in members:
                    friendly_list.append(f"ID: {member.id} NAME: {member.name}")

                await itr.followup.send(content=str(friendly_list))
                return

            case "default":
                await itr.response.send_message(
                    "Dev comamnd failed. Couldn't find a subcommand matching your input.",
                    ephemeral=True,
                )


async def setup(bot: models.BouncerBot):
    await bot.add_cog(Admin(bot))
