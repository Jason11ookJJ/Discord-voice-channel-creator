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
        if hasattr(error, 'original'):
            if hasattr(error, 'code'):
                if error.original.code == 50035:
                    embed_var = discord.Embed(title="Command error", description=f"""
                                        Maximum number of channels in category reached (50)
                                        """, color=0xff0f0f)
                    await ctx.send(embed=embed_var)
                    return
                elif error.original.code == 30013:
                    embed_var = discord.Embed(title="Command error", description=f"""
                                        Maximum number of guild channels reached (500)
                                        """, color=0xff0f0f)
                    await ctx.send(embed=embed_var)
                    return
        if isinstance(error, BotMissingPermissions):  # checking which type of error it is
            embed_var = discord.Embed(title="Command error", description=f"""
                    {error} It seems that I don't have enough permission to do this, please sent a message to the 
                     server admin to fix this problem. Enter "vc permission" to check for the permission that I need. 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
        elif isinstance(error, CommandNotFound):
            embed_var = discord.Embed(title="Command error", description=f"""
                    {str(error)}
                    All commands are cAsE sEnSitIvE, enter "vc help" for more 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
            db.save_error(ctx, error)
        else:
            embed_var = discord.Embed(title="Unknown error", description=f""" An unexpected error 
            occurred, please report this issue on [GitHub](
            https://github.com/Jason11ookJJ/Discord-voice-channel-creator/issues) OR join the [support server](
            https://discord.gg/P5Fd4KXXEJ), we will fix it soon 
                    """, color=0xff0f0f)
            await ctx.send(embed=embed_var)
            db.save_error(ctx, error)


def setup(bot):
    bot.add_cog(Error(bot))
