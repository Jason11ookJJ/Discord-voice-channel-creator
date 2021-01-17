import sqlite3
from discord.errors import HTTPException
from discord.ext import commands
import discord
import re

conn = sqlite3.connect('data.db')
db = conn.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS vc_channel(channel_id int, msg_channel int, respone_msg_id int)''')

class vc(commands.Cog, name = "Voice Channel"):
    def __init__(self, bot):
        self.bot = bot
    
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Channel cog is ready")

    # Commands
    @commands.command(brief='Create a voice channel',
                      description='Create a voice channel that only certain role can speak')
    
    async def create(self, ctx):
        msg = ctx.message
        channel_name = ""
        mention = msg.role_mentions + msg.mentions
        mention_name = []

        if mention != []: # @role
            if check_in_role(msg.author.id, msg.role_mentions):
                # create channel
                channel_name = re.sub('[@]', '', msg.clean_content[11:])
                new_channel = await msg.channel.category.create_voice_channel(channel_name)

                # setting permission
                for i in mention:
                    await new_channel.set_permissions(i, speak = True)
                    mention_name.append(i.name)
                mention_name = ", ".join(mention_name)

                await new_channel.set_permissions(ctx.guild.roles[0], speak = False)
            else: # not member of @role
                embedVar = discord.Embed(title="", description=f"""
                    {msg.author.mention}
                    You are not a member of that role,
                    Please ping another role or people
                    """, color=0xff0f0f)
                await msg.channel.send(embed=embedVar)
                return
        else: # only text
            channel_name = msg.clean_content[10:]
            if channel_name == "":
                channel_name = "created by voice channel creator"
            new_channel = await msg.channel.category.create_voice_channel(channel_name)
            mention_name = "everyone"

        embedVar = discord.Embed(title="", description=f"""
                    Created a voice channel
                    Name: {channel_name}
                    Speaker: {mention_name}

                    Creator: {msg.author.mention}
                    """, color=0x0ae0fc)
        respone_msg = await msg.channel.send(embed=embedVar)

        db.execute("INSERT INTO vc_channel(channel_id, msg_channel, respone_msg_id) VALUES (?, ?, ?)", (new_channel.id, msg.channel.id, respone_msg.id))
        conn.commit()

        try:
            await ctx.author.move_to(new_channel)
        except HTTPException: # User not connect to voice
            pass
   
    @commands.Cog.listener()
    async def on_voice_state_update(self, client, before, after):
        if before.channel is not None:
            channel_list = list(sum(db.execute("SELECT channel_id FROM vc_channel").fetchall(), ()))
            if before.channel.id in channel_list:
                if before.channel.members == []:
                    await before.channel.delete()
                    result = db.execute("SELECT msg_channel, respone_msg_id FROM vc_channel WHERE channel_id = (?)", [before.channel.id]).fetchall()[0]
                    msg_channel = self.bot.get_channel(result[0])
                    response_msg = await msg_channel.fetch_message(result[1])
                    description = response_msg.embeds[0].description

                    embedVar = discord.Embed(title="", description=f"""
                    (deleted) {description} 
                    """, color=0x0ae0fc)
                    await response_msg.edit(embed=embedVar)

                    db.execute("DELETE FROM vc_channel WHERE channel_id = (?)", [before.channel.id])
                    conn.commit()

def setup(bot):
    bot.add_cog(vc(bot))

def check_in_role(id, role):
    role_member = []
    for i in role:
        for q in i.members:
            role_member.append(q.id)

        if id not in role_member:
            return False
    
    return True