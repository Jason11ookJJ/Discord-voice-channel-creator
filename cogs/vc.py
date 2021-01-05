import sqlite3
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError

conn = sqlite3.connect('data.db')
db = conn.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS vc_channel(channel_id int, msg_channel int)''')

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
    
    async def create(self, ctx, role):
        msg = ctx.message
        channel_name = ""
        mention = msg.role_mentions + msg.mentions
        if mention != []: # @role
            if check_in_role(msg.author.id, msg.role_mentions):
                for i in mention:
                    channel_name = channel_name + " " + i.name
                q = msg.clean_content.split(" ")
                for i in range(2, len(q)):
                    if "@" not in q[i]:
                        channel_name = channel_name + " " + q[i]
                new_channel = await msg.channel.category.create_voice_channel(channel_name)

                # setting permission
                for i in mention:
                    await new_channel.set_permissions(i, speak = True)
                await new_channel.set_permissions(ctx.guild.roles[0], speak = False)
            else:
                await ctx.send("You are not in that role, @ a role that you are in")
                return
        else: # only text
            q = msg.clean_content.split(" ")
            for i in range(2, len(q)):
                if "@" not in q[i]:
                    channel_name = channel_name + " " + q[i]
            new_channel = await msg.channel.category.create_voice_channel(channel_name)
        db.execute("INSERT INTO vc_channel(channel_id, msg_channel) VALUES (?, ?)", (new_channel.id, msg.channel.id))
        conn.commit()

        await msg.channel.send("created a voice channel for \"" + channel_name +"\"")
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
                    # TODO send message to msg_channel when delete
                    msg_channel = list(sum(db.execute("SELECT msg_channel FROM vc_channel WHERE channel_id = (?)", [before.channel.id]).fetchall(), ()))[0]
                    msg_channel = self.bot.get_channel(msg_channel)
                    db.execute("DELETE FROM vc_channel WHERE channel_id = (?)", [before.channel.id])
                    await msg_channel.send(f"\"{before.channel.name}\" was deleted due to there is no member in that voice channel")
                    conn.commit()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        db.close()
        conn.close()
        await self.bot.logout()

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