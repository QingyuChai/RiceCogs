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

    @commands.command()
    async def buttfuck(self, user : discord.Member):
        """
        Fucks somebody in the... uhh... butt."""
        msg = "```\n"
        msg += user.name+ " met Shrek.\n"
        msg += "He was only 9 years old.\n"
        msg += "He loved Shrek so much,\n"
        msg += "he had all the merchandise and movies.\n"
        msg += "He prayed to Shrek every night before bed,\n"
        msg += "thanking him for the life he's been given.\n"
        msg += "\"Shrek is love\", he says; \"Shrek is life\".\n```"
        await self.bot.say(msg)
    @commands.command()
    async def rape(self, user : discord.Member):
        """
        Fucking without... consent!?"""
        await self.bot.say("```\n" + user.name + " gets raped.\n```")


def setup(bot):
    bot.add_cog(Kill(bot))