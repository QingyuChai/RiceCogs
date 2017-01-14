import discord

from cogs.utils import checks 
from discord.ext import commands
 
class Config:
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    @checks.is_owner()
    async def notify(self, *, content):
        """Notifies every server"""
        if content == "shutdown":
            for server in self.bot.servers:
                try:
                    await self.bot.send_message(server, "riceBot shutting down... Will be up again soon!")   #replace this riceBot with the name of your bot
                except discord.errors.Forbidden:
                    pass
        else:  
            for server in self.bot.servers:
                try:
                    await self.bot.send_message(server, content)
                except discord.errors.Forbidden:
                    pass
        await self.bot.say("Message succesfully sent")
    

    @commands.command()
    @checks.is_owner()
    async def say(self, *, content):
        """Says something"""
        await self.bot.say(content)
def setup(bot):
    bot.add_cog(Config(bot))