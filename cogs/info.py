import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog is ready")

    # Commands
    '''
    @commands.command(pass_content=True)
    async def help(self, ctx):
        channel = ctx.channel
        embedVar = discord.Embed(title="How to use?", description="", color=0x00ff00)
        embedVar.add_field(name="Voice channel", value="create <role>\ncreate a voice channel that only <role> can speak", inline=False)
        embedVar.add_field(name="Common", value="help\nShows this message\n\nchange_log\nGet the bot change log", inline=False)
        embedVar.add_field(name="Project Source code", value="https://github.com/Jason11ookJJ/Discord-voice-channel-creator", inline=False)
        embedVar.add_field(name="Creator of this bot", value="Jason11ookJJ#3151", inline=False)
        await channel.send(embed=embedVar)
    '''

    @commands.command()    
    async def change_log(self, ctx):
        channel = ctx.channel
        embedVar = discord.Embed(title="Change Log", description="", color=0x0ae0fc)
        embedVar.add_field(name="Pre release 0.1.2", value="Solve temp channel will not be closed after restart", inline=False)
        await channel.send(embed=embedVar)

def setup(bot):
    bot.add_cog(info(bot))