import discord
from cogs.utils.chat_formatting import box

from discord.ext import commands

class Code:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["language", "lng"])
    async def code(self, ctx, language, *, msg):
        """Makes your text in a codeblock in a certain language"""
        await self.bot.say(box(msg, language))

def setup(bot):
    bot.add_cog(Code(bot))
