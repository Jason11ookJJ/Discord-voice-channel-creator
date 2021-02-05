import discord
from discord.ext import commands
from package.function import current_time
from package.data import databaseDeo as db
import importlib


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner cog is ready")

    @commands.command(brief='Unload extension', description='Unload extension')
    @commands.is_owner()
    async def delete_all(self, ctx):
        channel_list = ctx.channel.category.channels
        for i in channel_list:
            if i != ctx.channel:
                await i.delete()


def setup(bot):
    bot.add_cog(Debug(bot))
