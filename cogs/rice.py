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
        msg = '```asciidoc\n'
        msg += '\n\nWhat is riceBot? :: '
        msg += '\nA friendly Discord bot based on Red that has a lot of handy features.'
        msg += 'The bot is currently on '
        msg += str(len(self.bot.servers))
        msg += ' Servers and connected to '
        msg += str(len(set(self.bot.get_all_members())))
        msg += ' users.\nHere is a list of basic commands:'
        msg += '\n```'
        msg += '```md\n'
        msg += '< Contact owner = use !contact [message]       >\n'
        msg += '< Get help      = use !help or !help [command] >\n'
        msg += '\n```'
        await self.bot.say(msg)
        
        link = '```markdown\n' 
        link += 'To add the bot to your own server, '
        link += 'open this [link](https://discordsites.com/ricebot/)'
        link += '\n```'
        await self.bot.say(link)

def setup(bot):
    bot.add_cog(riceBot(bot))