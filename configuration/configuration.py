import discord

from cogs.utils import checks
from discord.ext import commands

class Config:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def countservers(self):
        """
        Checks how many servers the bot is on"""
        msg = "The bot is in **"
        msg += len(self.bot.servers)
        msg += "** servers."
        await self.bot.say(msg)

    @commands.command()
    @checks.is_owner()
    async def listservers(self):
        """
        Checks what servers the bot is on"""
        servers = self.bot.servers
        await self.bot.say("```asciidoc\nThe bot is in the following servers:\n```")
        msg = "```asciidoc\n"
        #msg += "\n"
        for server in self.bot.servers:
            if len(server.members)<10:
                msg += "{:<1} :: 000{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members)<100:
                msg += "{:<1} :: 00{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members)<1000:
                msg += "{:<1} :: 0{} users :: {}".format(server.id, len(server.members), server.name)
            else:
                msg += "{:<1} :: {} users :: {}".format(server.id, len(server.members), server.name)
            msg += "\n"
        msg += "\n```"
        await self.bot.say(msg)


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def discrim(self, ctx, discriminator):
        """
        Find users with this discriminator"""
        msg = "Users with discriminator " + discriminator
        msg += ": \n"
        for r in self.bot.get_all_members():
            if r.discriminator == discriminator:
                if r.name in msg:
                    pass
                else:
                    msg += "```\n"
                    msg += r.name
                    msg += "\n```"
        await self.bot.say(msg)


    @commands.command()
    async def countusers(self):
        """
        Checks how many users the bot is connected to"""
        msg = "The bot is connected to **"
        msg += len(set(self.bot.get_all_members()))
        msg += "** users."
        await self.bot.say(msg)

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
