import discord
import os

client = discord.Client()
channel_list = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    channel = message.channel
    
    if message.author == client.user:
        return
    
    if message.content.startswith('vc'):
        msg = message.content.split(" ")
        if msg[1] == "create":
            if "@" in msg[2]:
                if message.mentions == []:
                    role = message.role_mentions
                    role_name = message.role_mentions[0].name
                    new_channel = await channel.category.create_voice_channel(role_name)
                    channel_list.append(new_channel.id)
                    
                    await new_channel.set_permissions(role[0], speak = True)
                    await new_channel.set_permissions(message.guild.roles[0], speak = False)
                    await channel.send("created a voice channel for \"" + role_name +"\"")
                    await message.author.move_to(new_channel)
                    
                else:
                    await channel.send("Please ping a role not a person")

@client.event
async def on_voice_state_update(client, before, after):
    if before.channel is not None:
        if before.channel.id in channel_list:
            await before.channel.delete()

client.run(os.environ['TOKEN'])
