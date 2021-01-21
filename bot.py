import discord
import os
from discord.ext import commands
import logging
from package.data import databaseDeo as db
import importlib

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='vc ', 
                    description='A voice channel bot created by Jason11ookJJ#3151', 
                    help_command=commands.DefaultHelpCommand(no_category = 'help'),
                    intents=intents)

bot.owner_id = int(os.environ["OWNER"])

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="vc help"))

@bot.command(brief='Load extension', description='Load extension')
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'package.cogs.{extension}')
    importlib.reload(db)
    await ctx.author.send(f"{extension} loaded")
    await ctx.message.delete()
    print(f"Extension: {extension} loaded")

for filename in os.listdir('./package/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'package.cogs.{filename[:-3]}')

bot.run(os.environ['TOKEN'])
