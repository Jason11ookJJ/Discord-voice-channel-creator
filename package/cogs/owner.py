import discord
from discord.ext import commands
from .vc import db


class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner cog is ready")

    @commands.command(brief='Unload extension', description='Unload extension')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'package.cogs.{extension}')
        await ctx.author.send(f"{extension} unloaded")
        await ctx.message.delete()
        print(f"Extension: {extension} unloaded")

    @commands.command(brief='Reload extension', description='Reload extension')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'package.cogs.{extension}')
        self.bot.load_extension(f'package.cogs.{extension}')
        await ctx.author.send(f"{extension} reloaded")
        await ctx.message.delete()
        print(f"Extension: {extension} reloaded")

    @commands.command()
    @commands.is_owner()
    async def stats(self, ctx):
        result = db.execute('''SELECT SUM(vc_created), SUM(vc_deleted) FROM full_statistic''').fetchall()
        created = result[0][0]
        deleted = result[0][1]
        embedVar = discord.Embed(title="Stats", description="", color=0x27AE60)
        embedVar.add_field(name="Server", value=f'''
                Server using this bot: {len(self.bot.guilds)}''', inline=False)

        embedVar.add_field(name="Voice channel", value=f'''
                Voice channel created: {created}        
                Voice channel deleted: {deleted}''', inline=False)
        await ctx.author.send(embed=embedVar)
        await ctx.message.delete()
        

def setup(bot):
    bot.add_cog(owner(bot))