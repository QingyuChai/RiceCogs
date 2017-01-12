import discord
from colors import red, green, blue

from discord.ext import commands

image = "data/ricebot/rice.jpg"

class riceBot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def countservers(self):
        """
        Checks how many servers the bot is on"""
        await self.bot.say(len(self.bot.servers))
    
    @commands.command()
    async def serverlist(self):
        """
        Checks what servers the bot is on"""
        await self.bot.say(self.bot.servers)
        


    @commands.command()
    async def countusers(self):
        """
        Checks how many users the bot is connected to"""
        await self.bot.say(len(set(self.bot.get_all_members())))    

    @commands.command(no_pm=True, pass_context=True)
    async def ricebot(self, ctx):
        """
        Shows bot info about riceBot"""
        channel = ctx.message.channel
        await self.bot.say('```asciidoc\n= riceBot =\n\nWhat is riceBot? :: \nA friendly Discord bot based on Red that has a lot of handy features. The bot is currently on ' + str(len(self.bot.servers)) + ' Servers and connected to ' + str(len(set(self.bot.get_all_members()))) + ' users.\nHere is a list of basic commands:\n``````md\n< Contact owner = use !contact [message]       >\n< Get help      = use !help or !help [command] >\n```', tts=False)
        await self.bot.say('```markdown\nTo add the bot to your own server, open this [link](https://discordsites.com/ricebot/)\n```')

def setup(bot):
    bot.add_cog(riceBot(bot))