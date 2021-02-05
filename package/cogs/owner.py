import discord
from discord.ext import commands
from package.function import current_time
from package.data import databaseDeo as db
import importlib


class Owner(commands.Cog):
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
            self.bot.unload_extension(f'cogs.{extension}')
            await ctx.message.add_reaction("✅")
            print(f"Extension: {extension} unloaded")
        except Exception as e:
            print(f"{current_time()} Extension: unload - {e}")
            await ctx.message.add_reaction("🛑")

    @commands.command(brief='Reload extension', description='Reload extension')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'package.cogs.{extension}')
            importlib.reload(db)
            await ctx.message.add_reaction("✅")
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
        embed_var = discord.Embed(title="Stats", description=f"Result generated: {current_time()}", color=0x27AE60)
        embed_var.add_field(name="Server", value=f'''
                Server using this bot: {len(self.bot.guilds)}''', inline=False)

        embed_var.add_field(name="Voice channel", value=f'''
                Voice channel created: {created}        
                Voice channel deleted: {deleted}''', inline=False)
        await ctx.channel.send(embed=embed_var)

    @commands.command()
    @commands.is_owner()
    async def resetdb(self, ctx):
        db.reset_db(self)
        print(f"{current_time()} DB: Reset Database (by {ctx.author.name})")
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def error(self, ctx):
        result = db.get_all_error()
        embed_var = discord.Embed(title="Error", description=f"Result generated: {current_time()}", color=0x27AE60)
        for i in result:
            embed_var.add_field(name=i[0], value=f'''
                    {i[2]}
                    {i[3]}''', inline=False)
        await ctx.channel.send(embed=embed_var)


def setup(bot):
    bot.add_cog(Owner(bot))
