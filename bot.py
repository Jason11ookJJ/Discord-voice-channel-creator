from discord.ext import commands
import discord
import os

bot = commands.Bot(command_prefix='vc ', description='A voice channel bot created by Jason11ookJJ#3151')
bot.remove_command('help')
channel_list = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="vc help"))


@bot.command()
async def create(ctx, role):
    if role == None:
        await ctx.send("Usage: vc create @role")
    else:
        msg = ctx.message
        channel_name = ""
        if msg.role_mentions != []:
            for i in msg.role_mentions:
                channel_name = channel_name + " " + i.name
            new_channel = await msg.channel.category.create_voice_channel(channel_name)
            channel_list.append(new_channel.id)
            for i in msg.role_mentions:
                await new_channel.set_permissions(i, speak = True)
            await new_channel.set_permissions(ctx.guild.roles[0], speak = False)
            await msg.channel.send("created a voice channel for \"" + channel_name +"\"")
            await ctx.author.move_to(new_channel)
    
@bot.command(pass_context=True)    
async def help(ctx):
    channel = ctx.channel
    embedVar = discord.Embed(title="How to use?", description="", color=0x00ff00)
    embedVar.add_field(name="Voice channel", value="create <role>\ncreate a voice channel that only <role> can speak", inline=False)
    embedVar.add_field(name="Common", value="help\nShows this message", inline=False)
    embedVar.add_field(name="Project Source code", value="https://github.com/Jason11ookJJ/Discord-voice-channel-creator", inline=False)
    embedVar.add_field(name="Creator of this bot", value="Jason11ookJJ#3151", inline=False)
    await channel.send(embed=embedVar)
            
@bot.event
async def on_voice_state_update(client, before, after):
    if before.channel is not None:
        if before.channel.id in channel_list:
            await before.channel.delete()

bot.run(os.environ['TOKEN'])
