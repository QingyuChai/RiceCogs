"""Birthday cog"""
import discord
import os
import datetime
import time
import asyncio

from __main__ import send_cmd_help
from .utils.chat_formatting import *
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Birthday:
    def __init__(self, bot):
        self.bot = bot
        self.day = "data/account/birthday.json"
        self.riceCog = dataIO.load_json(self.day)
        self.bot.say("Checking for Birthdays...")
        global loopistrue
        loopistrue = False

    async def _check_date(self):
        now = datetime.datetime.now()
        user_count = 0
        users_today = ""
        for users in self.riceCog:
            user = discord.utils.get(self.bot.get_all_members(), id=users)
            if now.day == self.riceCog[users]["day"] and now.month == self.riceCog[users]["month"]:
                msg = "Happy Birthday!"
                await self.bot.send_message(user, msg)
                user_count += 1
                user_day = user.name
                users_today += "{} has their birthday today!\n".format(user.name)
        if msg:
            if user_count == 1:
                await self.bot.say("{} is the only one who has their birthday today!".format(user_day))
            else:
                await self.bot.say("{} users have birthday today!".format(user_count))
                await self.bot.say(users_today)
        else:
            await self.bot.say("Nobody has birthday today!")

    @commands.group(pass_context=True)
    async def birthday(self, ctx):
        """
        Birthday options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @birthday.command(pass_context=True, name="set")
    async def _set(self, ctx, day, month, year):
        """
        Set your birthday"""
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            await self.bot.say("You did not enter a number. Try again.")
            return
        if month > 12 or month < 1:
            await self.bot.say("You did not enter a valid date. Try again.")
            return
        if day > 31 or day < 1:
            await self.bot.say("You did not enter a valid date. Try again.")
            return
        if year < 1940 or year > 2017:
            await self.bot.say("You did not enter a valid date. Try again.")
            return

        author = ctx.message.author
        if author.id not in self.riceCog or self.riceCog[author.id] == False:
            self.riceCog[author.id] = {}
            dataIO.save_json(self.day, self.riceCog)
        self.riceCog[author.id].update({"day" : day})
        self.riceCog[author.id].update({"month" : month})
        self.riceCog[author.id].update({"year" : year})
        dataIO.save_json(self.day, self.riceCog)
        day = self.riceCog[author.id]["day"]
        month = self.riceCog[author.id]["month"]
        year = self.riceCog[author.id]["year"]
        await self.bot.say("Your birthday is: {}/{}/{} (DD/MM/YY).".format(day, month, year))

    @birthday.command(pass_context=True, name="remove", aliases=["del", "rem"])
    async def _remove(self, ctx):
        author = ctx.message.author
        if author.id not in self.riceCog or self.riceCog[author.id] == False:
            await self.bot.say("You did not set your birthday yet!")
            return
        else:
            self.riceCog[author.id] = False
            dataIO.save_json(self.day, self.riceCog)
            await self.bot.say("Birthday succesfully removed!")


    @birthday.command(pass_context=True)
    async def show(self, ctx, *, user: discord.Member=None):
        """
        Show the birthday of a user"""
        author = ctx.message.author
        prefix = ctx.prefix
        if user == None:
            user = author
        if user.id in self.riceCog and self.riceCog[user.id] != False:
            day = self.riceCog[user.id]["day"]
            month = self.riceCog[user.id]["month"]
            year = self.riceCog[user.id]["year"]
            await self.bot.say(str(user.name) + "'s birthday is: {}/{}/{} (DD/MM/YY).".format(day, month, year))
        else:
            msg = "You have not set your birthday yet! Do it now with {}birthday set!".format(prefix)
            await self.bot.say(msg)

    @checks.is_owner()
    @birthday.command()
    async def dmloop(self):
        global loopistrue
        if loopistrue:
            await self.bot.say("There is a loop going on right now!")
            return
        else:
            loopistrue = True
        global loopedieloop
        loopedieloop = True
        while loopedieloop:
            await self._check_date()
            await asyncio.sleep(86400)

    def __unload(self):
        global loopedieloop
        loopedieloop = False
        print("Stopped checking for birthdays...")




def check_folder():
    if not os.path.exists("data/account"):
        print("Creating data/account folder")
        os.makedirs("data/account")

def check_file():
    data = {}
    f = "data/account/birthday.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/account/birthday.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    n = Birthday(bot)
    bot.add_cog(n)
