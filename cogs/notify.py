import discord

from cogs.utils import checks 
from discord.ext import commands
 
class Notify:
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    @checks.is_owner()
    async def notify(self, *, content):
        """Notifies every server"""
        for server in self.bot.servers:
            await self.bot.send_message(server, content)
def setup(bot):
    bot.add_cog(Notify(bot))