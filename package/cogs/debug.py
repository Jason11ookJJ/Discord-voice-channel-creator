from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner cog is ready")

    @commands.command(brief='delete all channel in this category', description='delete all channel in this category')
    @commands.is_owner()
    async def delete_all(self, ctx):
        channel_list = ctx.channel.category.channels
        for i in channel_list:
            if i != ctx.channel:
                await i.delete()


def setup(bot):
    bot.add_cog(Debug(bot))
