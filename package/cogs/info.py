import discord
from discord.ext import commands
import json

with open('package/data/change_log.json') as f:
    data = json.load(f)

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
        msg = ctx.message.clean_content.split(" ")
        version = "0.1.6"
        if len(msg) > 2:
            version = msg[2]
        description = data.get(version)
        if description != None:
            embedVar = discord.Embed(title="Change Log", description="", color=0x0ae0fc)
            embedVar.add_field(name= "v" + version, value=description,
                    inline=False)
            await channel.send(embed=embedVar)
        else:
            embedVar =  discord.Embed(title="", description=f"""
                    {ctx.author.mention}
                    Incorrect version nummber.
                    Usage: vc change_log [version_number]
                    """, color=0xff0f0f)
            await channel.send(embed = embedVar)

def setup(bot):
    bot.add_cog(info(bot))