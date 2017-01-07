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
        await self.bot.say(" " + user.mention + " gets " + random.choice(my_array) + ".", tts=False)

    @commands.command()
    async def buttfuck(self, user : discord.Member):
        """
        Fucks somebody in the... uhh... butt."""
        await self.bot.say(user.mention + " met Shrek.")
        await self.bot.say("He was only 9 years old")
        await self.bot.say("He loved Shrek so much, He had all the merchandise and movies")
        await self.bot.say("He prayed to Shrek every night before bed, thanking him for the life he's been given")
        await self.bot.say("\"Shrek is love\" he says; \"Shrek is life\"")
    @commands.command()
    async def rape(self, user : discord.Member):
        """
        Fucking without... consent!?"""
        await self.bot.say(user.mention + " gets raped.")


def setup(bot):
    bot.add_cog(Kill(bot))
 