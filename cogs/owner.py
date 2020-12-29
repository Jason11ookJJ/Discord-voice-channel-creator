import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner cog is ready")

    @commands.command(brief='Load extension', description='Load extension')
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.channel.send(f"{extension} loaded")

    @commands.command(brief='Unload extension', description='Unload extension')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')

    @commands.command(brief='Reload extension', description='Reload extension')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')

def setup(bot):
    bot.add_cog(owner(bot))