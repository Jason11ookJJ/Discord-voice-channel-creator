import sqlite3
from discord.ext import commands

conn = sqlite3.connect('data.db')
db = conn.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS channel(id String)''')

class vc(commands.Cog, name = "Voice Channel"):
    def __init__(self, bot):
        self.bot = bot
    
    # enent
    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Channel cog is ready")

    # Commands
    @commands.command(brief='Create a voice channel', description='Create a voice channel that only certain role can speak')
    async def create(self, ctx, role):
        msg = ctx.message
        if msg.role_mentions == []:
            await ctx.send("Usage: vc create @role")
        else:
            channel_name = ""
            if check_in_role(msg.author.id, msg.role_mentions):
                for i in msg.role_mentions:
                    channel_name = channel_name + " " + i.name
                new_channel = await msg.channel.category.create_voice_channel(channel_name)
                db.execute("INSERT INTO channel VALUES (?)", [new_channel.id])    
                conn.commit()

                for i in msg.role_mentions:
                    await new_channel.set_permissions(i, speak = True)
                await new_channel.set_permissions(ctx.guild.roles[0], speak = False)
                await msg.channel.send("created a voice channel for \"" + channel_name +"\"")
                await ctx.author.move_to(new_channel)
            else:
                await ctx.send("You are not in that role, @ a role that you are in")
                
    @commands.Cog.listener()
    async def on_voice_state_update(self, client, before, after):
        if before.channel is not None:
            channel_list = list(sum(db.execute("SELECT id FROM channel").fetchall(), ()))
            if before.channel.id in channel_list:
                if before.channel.members == []:
                    await before.channel.delete()
                    db.execute("DELETE FROM channel WHERE id = (?)", [before.channel.id])
    
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