from traceback import print_stack
import discord
from discord.ext import commands
from ..function import current_time
from ..data import databaseDeo as db
import importlib

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner cog is ready")

    @commands.command(brief='Unload extension', description='Unload extension')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'package.cogs.{extension}')
            await ctx.author.send(f"{extension} unloaded")
            print(f"Extension: {extension} unloaded")
        except Exception as e:
            print(f"{current_time()} Extension: unload - {e}")
            await ctx.message.add_reaction("🛑")
        
    @commands.command(brief='Reload extension', description='Reload extension')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'package.cogs.{extension}')
            self.bot.load_extension(f'package.cogs.{extension}')
            importlib.reload(db)
            await ctx.author.send(f"{extension} reloaded")
            print(f"Extension: {extension} reloaded")
        except Exception as e:
            print(f"{current_time()} Extension: reload - {e}")
            await ctx.message.add_reaction("🛑")
        

    @commands.command()
    @commands.is_owner()
    async def stats(self, ctx):
        result = db.get_all_stats()
        created = result[0][0]
        deleted = result[0][1]
        embedVar = discord.Embed(title="Stats", description=f"Result generated: {current_time()}", color=0x27AE60)
        embedVar.add_field(name="Server", value=f'''
                Server using this bot: {len(self.bot.guilds)}''', inline=False)

        embedVar.add_field(name="Voice channel", value=f'''
                Voice channel created: {created}        
                Voice channel deleted: {deleted}''', inline=False)
        await ctx.channel.send(embed = embedVar)
    
    @commands.command()
    @commands.is_owner()
    async def resetdb(self, ctx):
        db.resetDB()
        print(f"{current_time()} DB: Reset Database (by {ctx.author.name})")
        

def setup(bot):
    bot.add_cog(owner(bot))