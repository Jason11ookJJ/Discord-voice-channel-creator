import discord
from discord.ext import commands
from package.function import current_time, time_zone_time
from package.data import databaseDeo as db


class Vc(commands.Cog, name="Voice Channel"):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Channel cog is ready")

    # Commands
    @commands.command(brief='Create a voice channel',
                      description='Create a voice channel that only certain role can speak')
    @commands.bot_has_permissions(read_messages=True,
                                  manage_messages=True,
                                  manage_roles=True,
                                  manage_channels=True,
                                  send_messages=True,
                                  view_channel=True,
                                  embed_links=True)
    async def create(self, ctx):
        check = await check_in_role(ctx)
        if check == 2 or check == 0:
            i = await create_voice(ctx)
            if i:
                new_channel = i.get("new_channel")
                embed_var = discord.Embed(title="", description=f"""
                                        Vcc common
                                        Name: {str(new_channel)}
                                        Speaker: {i.get("mention_name")}
                                        Creator: {ctx.author.mention}
        
                                        Started: {time_zone_time(ctx)}
                                        """, color=0x0ae0fc)
                response_msg = await ctx.channel.send(embed=embed_var)

                db.save_voice_channel(new_channel.id, ctx.channel.id, response_msg.id)

                print(f"{current_time()} VC: a channel is created (created: 1, deleted: 0)")
                save(self, 1, 0)

    @commands.command(brief='Create a private voice channel',
                      description='Create a private voice channel that only certain role can speak and hear')
    @commands.bot_has_permissions(read_messages=True,
                                  manage_messages=True,
                                  manage_roles=True,
                                  manage_channels=True,
                                  send_messages=True,
                                  view_channel=True,
                                  embed_links=True)
    async def private(self, ctx):
        check = await check_in_role(ctx)
        if check == 0:
            i = await create_voice(ctx)
            if i:
                j = await create_text(ctx)
                if j:
                    new_channel = i.get("new_channel")
                    text_channel = j.get("new_channel")

                    # set permission
                    for q in i.get("mention"):
                        await new_channel.set_permissions(q, connect=True)
                        await text_channel.set_permissions(q, read_messages=True)
                    await new_channel.set_permissions(ctx.guild.roles[0], connect=False)
                    await text_channel.set_permissions(ctx.guild.roles[0], read_messages=False)
                    await new_channel.set_permissions(self.bot.users[0], connect=True)
                    await text_channel.set_permissions(self.bot.users[0], read_messages=True)

                    embed_var = discord.Embed(title="", description=f"""
                                                Vcc private
                                                Name: {str(new_channel)}
                                                Speaker + Listener: {i.get("mention_name")}
                                                Creator: {ctx.author.mention}
            
                                                Started: {time_zone_time(ctx)}
                                                """, color=0x178fff)
                    response_msg = await ctx.channel.send(embed=embed_var)

                    db.save_text_channel(new_channel.id, text_channel.id)
                    db.save_voice_channel(new_channel.id, ctx.channel.id, response_msg.id)
                    print(f"{current_time()} VC: a private channel is created (created: 1, deleted: 0)")
                    save(self, 1, 0)
        elif check == 2:
            embed_var = discord.Embed(title="", description=f"""
                                                {ctx.author.mention}
                                                You need to ping a user to create a private channel, use "vc create" instead 
                                                """, color=0xff0f0f)
            await ctx.channel.send(embed=embed_var)

    @commands.command(brief='Create a voice and text channel',
                      description='Create a voice channel that only certain role can speak')
    @commands.bot_has_permissions(read_messages=True,
                                  manage_roles=True,
                                  manage_messages=True,
                                  manage_channels=True,
                                  send_messages=True,
                                  view_channel=True,
                                  embed_links=True)
    async def text(self, ctx):
        check = await check_in_role(ctx)
        if check == 2 or check == 0:
            i = await create_voice(ctx)
            q = await create_text(ctx)
            if i and q:
                voice_channel = i.get("new_channel")
                embed_var = discord.Embed(title="", description=f"""Vcc text and voice
                                                                    Name: {str(voice_channel)}
                                                                    Speaker: {i.get("mention_name")}
                                                                    Creator: {ctx.author.mention}
                                        
                                                                    Started: {time_zone_time(ctx)}
                                                                    """, color=0x0ae0fc)
                response_msg = await ctx.channel.send(embed=embed_var)
                db.save_voice_channel(voice_channel.id, ctx.channel.id, response_msg.id)
                db.save_text_channel(voice_channel.id, q.get("new_channel").id)
                print(f"{current_time()} VC: a channel is created (created: 1, deleted: 0)")
                save(self, 1, 0)

    @commands.Cog.listener()
    async def on_voice_state_update(self, client, before, after):
        if before.channel is not None:
            result = db.get_channel(before.channel.id)
            if result:
                if not before.channel.members:
                    await before.channel.delete()

                    # delete text channel
                    tx_channel_id = result.get("tx_channel_id")
                    if tx_channel_id:
                        tx_channel = self.bot.get_channel(tx_channel_id)
                        await tx_channel.delete()

                    # edit message
                    msg_channel = self.bot.get_channel(result.get("msg_channel_id"))
                    response_msg = await msg_channel.fetch_message(result.get("response_msg_id"))
                    embeds = response_msg.embeds
                    if embeds:
                        description = embeds[0].description

                        embed_var = discord.Embed(title="", description=f"""
                        (deleted) {description} 
                        Ended: {time_zone_time(before.channel)}
                        """, color=0x129eb0)
                        await response_msg.edit(embed=embed_var)

                    db.delete_channel(before.channel.id)

                    print(f"{current_time()} VC: a channel is deleted (created: 0, deleted: 1)")
                    save(self, 0, 1)


async def create_voice(ctx):
    msg = ctx.message
    mention = msg.role_mentions + msg.mentions
    mention_list = []
    channel_name = await get_channel_name(msg)
    if channel_name == "":
        channel_name = "created by Vcc"

    if msg.channel.category is None:  # not a channel in category
        new_channel = await msg.channel.guild.create_voice_channel(channel_name)
    else:  # channel in category
        new_channel = await msg.channel.category.create_voice_channel(channel_name)

    if mention:  # @role
        await new_channel.set_permissions(ctx.guild.roles[0], speak=False)

    # setting permission
    for i in mention:
        await new_channel.set_permissions(i, speak=True)
        mention_list.append(i.mention)
    mention_name = ", ".join(mention_list)
    if not mention_name:
        mention_name = "everyone"

    mention.append(msg.author)
    if ctx.author.voice:
        await ctx.author.move_to(new_channel)

    return {"new_channel": new_channel, "mention": mention, "mention_name": mention_name}


async def create_text(ctx):
    msg = ctx.message
    mention = msg.role_mentions + msg.mentions
    channel_name = await get_channel_name(msg)
    if channel_name == "":
        channel_name = "created by Vcc"

    if msg.channel.category is None:
        new_channel = await msg.channel.guild.create_text_channel(channel_name)
    else:
        new_channel = await msg.channel.category.create_text_channel(channel_name)

    # setting permission
    for i in mention:
        await new_channel.set_permissions(i, send_messages=True)

    await new_channel.set_permissions(ctx.guild.roles[0], send_messages=False)

    return {"new_channel": new_channel}


async def get_channel_name(msg):
    channel_name = " ".join(msg.clean_content.split(" ")[2:])
    if len(channel_name) > 100:
        embed_var = discord.Embed(title="", description=f"""
                                            {msg.author.mention}
                                            Channel name is too long (Max: 100 characters)
                                            """, color=0xff0f0f)
        await msg.channel.send(embed=embed_var)
    return channel_name


def save(self, created, deleted):
    server_count = len(self.bot.guilds)
    db.stats_save(server_count, created, deleted)


async def check_in_role(ctx):
    """
    return
    0: in all role
    1: not in some role
    2: no mention
    """
    mention = ctx.message.role_mentions
    author_role = ctx.author.roles
    if not mention and ctx.message.mentions == []:
        return 2
    for i in mention:
        if i not in author_role:
            embed_var = discord.Embed(title="", description=f"""
                                    {ctx.author.mention}
                                    You are not a member of that role,
                                    Please ping another role or people
                                    """, color=0xff0f0f)
            await ctx.channel.send(embed=embed_var)
            return 1
    return 0


def setup(bot):
    bot.add_cog(Vc(bot))
