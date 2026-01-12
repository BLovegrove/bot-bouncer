from ast import Import
import discord
from discord.ext import commands
from loguru import logger

from util import cfg
from util.handlers.extensions import ExtensionHandler as Ext


class BouncerBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(intents=intents, command_prefix=commands.when_mentioned)
        self.command_list = Ext.search(Ext.Type.COMMAND)
        self.event_list = Ext.search(Ext.Type.EVENT)
        self.task_list = Ext.search(Ext.Type.TASK)

    # load cogs
    async def setup_hook(self) -> None:
        for command in self.command_list:
            await self.load_extension(command)

        for event in self.event_list:
            await self.load_extension(event)

        for task in self.task_list:
            await self.load_extension(task)

        logger.debug("Finished loading setup_hook")

        return await super().setup_hook()
