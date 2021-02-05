import discord
from discord.ext import commands
from discord.ext.commands import BotMissingPermissions, CommandNotFound
from package.data import databaseDeo as db


class Error(commands.Cog, name="Voice Channel"):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Error cog is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.message.add_reaction("🛑")
        if isinstance(error, BotMissingPermissions):  # checking which type of error it is
            embed_var = discord.Embed(title="Sorry, an error occurred", description=f"""
                    {error} It seems that I don't have enough permission to do this, please sent a message to the 
                     server admin to fix this problem. Enter "vc permission" to check for the permission that I need. 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
        elif isinstance(error, CommandNotFound):
            embed_var = discord.Embed(title="Sorry, an error occurred", description=f"""
                    {ctx.message.clean_content.split(" ")[1]} Command not found
                    All commands are case-incentive, enter "vc help" for more 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
        else:
            embed_var = discord.Embed(title="Sorry, an unknown error occurred", description=f""" An unexpected error 
            occurred, please report this issue on [GitHub](
            https://github.com/Jason11ookJJ/Discord-voice-channel-creator/issues) OR join the [support server](
            https://discord.gg/P5Fd4KXXEJ), we will fix it soon 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
        db.save_error(ctx, error)


def setup(bot):
    bot.add_cog(Error(bot))
