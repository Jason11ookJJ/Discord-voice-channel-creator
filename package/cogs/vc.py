import re
import discord
from discord.errors import HTTPException
from discord.ext import commands, tasks
from ..function import current_time
from ..data import databaseDeo as db


class vc(commands.Cog, name = "Voice Channel"):
    def __init__(self, bot):
        global created, deleted
        created = 0
        deleted = 0
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Channel cog is ready")

    # Commands
    @commands.command(brief='Create a voice channel',
                      description='Create a voice channel that only certain role can speak')
    
    async def create(self, ctx):
        global created, deleted
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
                    Voice channel creator
                    Name: {channel_name}
                    Speaker: {mention_name}
                    Creator: {msg.author.mention}

                    Started: {current_time()}
                    """, color=0x0ae0fc)
        respone_msg = await msg.channel.send(embed=embedVar)

        db.savechannel(new_channel.id, msg.channel.id, respone_msg.id)
        
        try:
            await ctx.author.move_to(new_channel)
        except HTTPException: # User not connect to voice
            pass

        created += 1
        print(f"{current_time()} VC: a channel is created (created: {created}, deleted: {deleted})")
        save(self)
   
    @commands.Cog.listener()
    async def on_voice_state_update(self, client, before, after):
        global created, deleted
        if before.channel is not None:
            result = db.get_all_channel(before.channel.id)
            if result != "":
                if before.channel.members == []:
                    await before.channel.delete()
                    msg_channel = self.bot.get_channel(result[0][1])
                    response_msg = await msg_channel.fetch_message(result[0][2])
                    embeds = response_msg.embeds
                    if embeds != []:
                        description = embeds[0].description

                        embedVar = discord.Embed(title="", description=f"""
                        (deleted) {description} 
                        Ended: {current_time()}
                        """, color=0x0ae0fc)
                        await response_msg.edit(embed=embedVar)

                    db.deleteChannel(before.channel.id)
                    
                    deleted += 1
                    print(f"{current_time()} VC: a channel is deleted (created: {created}, deleted: {deleted})")
                    save(self)



def save(self):
    global created, deleted
    server_count = len(self.bot.guilds)
    db.statsSave(server_count, created, deleted)
    created = 0
    deleted = 0
    
def check_in_role(id, role):
    role_member = []
    for i in role:
        for q in i.members:
            role_member.append(q.id)

        if id not in role_member:
            return False
    
    return True

def setup(bot):
    bot.add_cog(vc(bot))
