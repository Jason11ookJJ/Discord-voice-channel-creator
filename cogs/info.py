import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog is ready")

    @commands.command(brief='Shows change log of newest version', description='Shows current version and change log')    
    async def change_log(self, ctx):
        channel = ctx.channel
        embedVar = discord.Embed(title="Change Log", description="", color=0x0ae0fc)
        embedVar.add_field(name="Pre release v0.1.5", value='''
                Added feature:
                1. the bot will alert the user when a voice channel is deleted
                ''',
                inline=False)
        await channel.send(embed=embedVar)

def setup(bot):
    bot.add_cog(info(bot))