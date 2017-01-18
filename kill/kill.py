import discord
import random

from discord.ext import commands
my_array = ["destroyed", "ripped apart", "cut into pieces", "brutally murdered", "annihilated", "raped", "buttfucked", "killed"]
class Kill:
    """Not so friendly"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kill(self, user : discord.Member):
        """
        Kills somebody"""
        await self.bot.say("```\n" + user.name + " gets " + random.choice(my_array) + ".\n```", tts=False)

    @commands.command(aliases = ["buttfuck"])
    async def shrek(self, user : discord.Member):
        """
        Fucks somebody in the... uhh... butt."""
        msg = "```\n"
        msg += user.name+ " met Shrek.\n"
        msg += "He was only 9 years old.\n"
        msg += "He loved Shrek so much.\n"
        msg += "He had all the merchandise and movies.\n"
        msg += "He prayed to Shrek every night before bed,\n"
        msg += "thanking him for the life he's been given.\n"
        msg += "\"Shrek is love\", he says; \"Shrek is life\".\n```"
        await self.bot.say(msg)

    @commands.command(aliases = ["od"], pass_context=True)
    async def overdose(self, ctx, user : discord.Member=None, *, stuff):
        """
        Have somebody overdose on something"""
        author = ctx.message.author
        if user == None:
            user = author
        msg = "```\n"
        msg += user.name
        msg += " overdosed on "
        msg += stuff
        msg += "."
        msg +="\n```"
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Kill(bot))
