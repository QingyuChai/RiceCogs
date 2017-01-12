import discord

from cogs.utils import checks 
from discord.ext import commands
 
class Config:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def game(self):
        status = list(self.bot.servers)[0].me.status
        game = game=discord.Game(name="with FwiedWice :3")
        await self.bot.change_presence(status=status, game=game)

 
    @commands.command()
    @checks.is_owner()
    async def notify(self, *, content):
        """Notifies every server"""
        if content == "shutdown":
            for server in self.bot.servers:
               await self.bot.send_message(server, "Bananya shutting down... Will be up again soon!")
            await self.bot.say("Message succesfully sent")
        else:  
            for server in self.bot.servers:
                await self.bot.send_message(server, content)
            await self.bot.say("Message succesfully sent")
    

    @commands.command()
    @checks.is_owner()
    async def say(self, *, content):
        """Says something"""
        await self.bot.say(content)
def setup(bot):
    bot.add_cog(Config(bot))