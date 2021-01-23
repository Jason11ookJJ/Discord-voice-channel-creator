from function import current_time
import discord
import os
from discord.ext import commands
import logging
from data import databaseDeo as db
import importlib
from dotenv import load_dotenv

load_dotenv()
os.getenv("OWNER")
os.getenv("TOKEN")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='vc ',
                   description='A voice channel bot created by Jason11ookJJ#3151',
                   help_command=commands.DefaultHelpCommand(no_category='help'),
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
    try:
        bot.load_extension(f'cogs.{extension}')
        importlib.reload(db)
        await ctx.message.add_reaction("✅")
        print(f"Extension: {extension} loaded")
    except Exception as e:
        print(f"{current_time()} Extension: load - {e}")
        await ctx.message.add_reaction("🛑")


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['TOKEN'])
