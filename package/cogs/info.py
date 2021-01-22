import discord
from discord.ext import commands
from ..data.change_log import change_log


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog is ready")

    @commands.command(brief='Shows change log of newest version', description='Shows current version and change log')    
    async def change_log(self, ctx):
        channel = ctx.channel
        msg = ctx.message.clean_content.split(" ")
        version = "0.7.1"
        if len(msg) > 2:
            version = msg[2]
        description = change_log.get(version)
        if description != None:
            embedVar = discord.Embed(title="Change Log", description="", color=0x0ae0fc)
            embedVar.add_field(name= "v" + version, value=description,
                    inline=False)
            await channel.send(embed=embedVar)
        else:
            embedVar =  discord.Embed(title="", description=f"""
                    {ctx.author.mention}
                    Incorrect version number.
                    Usage: vc change_log [version_number]
                    """, color=0xff0f0f)
            await channel.send(embed = embedVar)

    @commands.command(brief='Get permission needed to run the bot', description='Get permission needed to run the bot')    
    async def permission(self, ctx):
        embedVar =  discord.Embed(title="Permission", description=f"""
                    These are the permission needed to run me properly. Please enable them.
                    """, color=0xF2C94C)
        embedVar.add_field(name = "Lists", value="""
        - manage channels
        - view channel
        - send messages
        - manage messages
        - embed links
        - read message history
        - add reactions
        - connect
        - move member
        """)
        await ctx.send(embed = embedVar)

def setup(bot):
    bot.add_cog(info(bot))