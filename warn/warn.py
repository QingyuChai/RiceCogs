"""Warning cog"""

#Credits go to Twentysix26 for modlog
#https://github.com/Twentysix26/Red-DiscordBot/blob/develop/cogs/mod.py

import discord
import os
import shutil
import aiohttp
import asyncio
import os

from .utils.chat_formatting import *
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands
from enum import Enum
from __main__ import send_cmd_help

colour = '099999'
default_warn = ("user.mention, you have received your "
                "warning #warn.count! At warn.limit warnings you "
                "will be kicked!")
default_max = 3
default_kick = ("After warn.limit warnings, user.name has been kicked.")

class Warn:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/account/warnings.json"
        self.riceCog = dataIO.load_json(self.profile)
        self.warning_settings = "data/account/warning_settings.json"
        self.riceCog2 = dataIO.load_json(self.warning_settings)
        try:
            self._cog = self.bot.get_cog("Mod")
        except:
            print("You need the mod cog to properly run warn")

    @commands.group(no_pm=True, pass_context=True, name='warnset')
    async def _warnset(self, ctx):
        if ctx.message.server.id not in self.riceCog2:
            self.riceCog2[ctx.message.server.id] = {}
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            server = ctx.message.server
            try:
                msg = self.riceCog2[server.id]["warn_message"]
            except:
                msg = default_warn
            try:
                kick = self.riceCog2[server.id]["kick_message"]
            except:
                kick = default_kick
            try:
                _max = self.riceCog2[server.id]["max"]
            except:
                _max = default_max
            message =  "```\n"
            message += "Warn Message - {}\n"
            message += "Kick Message - {}\n"
            message += "Warn Limit   - {}\n"
            message += "```"
            await self.bot.say(message.format(msg, kick, _max))

    @_warnset.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(
      =True, manage_server=True)
    async def max(self, ctx, limit : int):
        server = ctx.message.server

        self.riceCog2[server.id]["max"] = limit
        dataIO.save_json(self.warning_settings, self.riceCog2)
        await self.bot.say("Warn limit is now: \n{}".format(limit))

    @_warnset.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(kick_members=True, manage_server=True)
    async def kick(self, ctx, *, msg=None):
        """Set the kick message.

        To get a full list of information, use **warnset message** without any parameters."""
        if not msg:
            await self.bot.say("```Set the kick message.\n\n"
                               "To get a full list of information, use **warnset message** without any parameters.```")
            return
        server = ctx.message.server

        self.riceCog2[server.id]["kick_message"] = msg
        dataIO.save_json(self.warning_settings, self.riceCog2)
        await self.bot.say("Kick message is now: \n{}".format(msg))

    @_warnset.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(kick_members=True, manage_server=True)
    async def reset(self, ctx):
        server = ctx.message.server
        author = ctx.message.author
        channel = ctx.message.channel
        await self.bot.say("Are you sure you want to reset all warn settings"
                           "for this server?\n"
                           "Type **yes** within the next 15 seconds.")
        msg = await self.bot.wait_for_message(author=author, channel=channel, timeout=15.0)
        if msg.content.lower().strip() == "yes":
            self.riceCog2[server.id]["warn_message"] = default_warn
            self.riceCog2[server.id]["kick_message"] = default_kick
            self.riceCog2[server.id]["max"] = default_max
        else:
            await self.bot.say("Nevermind then.")
            return

    @_warnset.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(kick_members=True, manage_server=True)
    async def message(self, ctx, *, msg = None):
        """Set the warning message

        user.mention - mentions the user
        user.name   - names the user
        user.id     - gets id of user
        warn.count  - gets the # of this warn
        warn.limit  - # of warns allowed

        Example:

        **You, user.mention, have received Warning warn.count. After warn.limit, you will be kicked.**

        You can set it either for every server.
        To set the kick message, use *warnset kick*
        """
        if not msg:
            await self.bot.say("```Set the warning message\n\n"
                               "user.mention - mentions the user\n"
                               "user.name   - names the user\n"
                               "user.id     - gets id of user\n"
                               "warn.count  - gets the # of this warn\n"
                               "warn.limit  - # of warns allowed\n\n"

                               "Example:\n\n"

                               "**You, user.mention, have received Warning warn.count. After warn.limit, you will be kicked.**\n\n"

                               "You can set it either for every server.\n"
                               "To set the kick message, use *warnset kick*\n")
            return


        server = ctx.message.server

        self.riceCog2[server.id]["warn_message"] = msg
        dataIO.save_json(self.warning_settings, self.riceCog2)
        await self.bot.say("Warn message is now: \n{}".format(msg))


    @commands.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(kick_members=True)
    async def warn(self, ctx, user : discord.Member, *, reason=None):
        """Warns the user - At 3 warnings the user gets kicked

        Thank you, 26, for the modlog"""
        server = ctx.message.server
        author = ctx.message.author
        channel = ctx.message.channel

        can_kick = channel.permissions_for(server.me).kick_members

        if can_kick:
            pass
        else:
            await self.bot.say("I'm not allowed to do that.")
            return

        if server.id not in self.riceCog2:
            msg = default_warn
            kick = default_kick
            _max = default_max
        try:
            msg = self.riceCog2[server.id]["warn_message"]
        except:
            msg = default_warn
        try:
            kick = self.riceCog2[server.id]["kick_message"]
        except:
            kick = default_kick
        try:
            _max = self.riceCog2[server.id]["max"]
        except:
            _max = default_max

        #checks if the user is in the file

        if server.id not in self.riceCog:
            self.riceCog[server.id] = {}
            dataIO.save_json(self.profile, self.riceCog)
            if user.id not in self.riceCog[server.id]:
                self.riceCog[server.id][user.id] = {}
                dataIO.save_json(self.profile, self.riceCog)
            else:
                pass
        else:
            if user.id not in self.riceCog[server.id]:
                self.riceCog[server.id][user.id] = {}
                dataIO.save_json(self.profile, self.riceCog)
            else:
                pass

        if "Count" in self.riceCog[server.id][user.id]:
            count = self.riceCog[server.id][user.id]["Count"]
        else:
            count = 0

        #checks how many warnings the user has
        if count != _max - 1:
            count += 1
            msg = msg.replace("user.mention", user.mention)
            msg = msg.replace("user.name", user.name)
            msg = msg.replace("user.id", user.id)
            msg = msg.replace("warn.count", str(count))
            msg = msg.replace("warn.limit", str(_max))
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            if reason:
                data.add_field(name="Reason", value=reason, inline=False)
            data.set_footer(text="riceBot")
            await self.bot.say(embed=data)
            self.riceCog[server.id][user.id].update({"Count" : count})
            dataIO.save_json(self.profile, self.riceCog)
            if reason:
                await self._cog.new_case(server,
                                    action="Warning #{}".format(count),
                                    mod=author,
                                    user=user,
                                    reason=reason)
            else:
                await self._cog.new_case(server,
                                    action="Warning #{}".format(count),
                                    mod=author,
                                    user=user)
        else:
            msg = kick
            msg = msg.replace("user.mention", user.mention)
            msg = msg.replace("user.name", user.name)
            msg = msg.replace("user.id", user.id)
            msg = msg.replace("warn.count", str(count))
            msg = msg.replace("warn.limit", str(_max))
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            if reason:
                data.add_field(name="Reason", value=reason, inline=False)
            data.set_footer(text="riceBot")
            await self.bot.say(embed=data)

            count = 0
            self.riceCog[server.id][user.id].update({"Count" : count})
            dataIO.save_json(self.profile, self.riceCog)
            if reason:
                await self._cog.new_case(server,
                                    action="Kicked after {} warnings.".format(_max),
                                    mod=author,
                                    user=user,
                                    reason=reason)
            else:
                await self._cog.new_case(server,
                                    action="Kicked after {} warnings.".format(_max),
                                    mod=author,
                                    user=user)
            await self.bot.kick(user)

    @commands.command(no_pm=True, pass_context=True)
    @checks.mod_or_permissions(kick_members=True)
    async def clean(self, ctx, user : discord.Member):
        author = ctx.message.author
        server = author.server

        if server.id not in self.riceCog:
            self.riceCog[server.id] = {}
            dataIO.save_json(self.profile, self.riceCog)
            if user.id not in self.riceCog[server.id]:
                self.riceCog[server.id][user.id] = {}
                dataIO.save_json(self.profile, self.riceCog)
            else:
                pass
        else:
            if user.id not in self.riceCog[server.id]:
                self.riceCog[server.id][user.id] = {}
                dataIO.save_json(self.profile, self.riceCog)
            else:
                pass

        if "Count" in self.riceCog[server.id][user.id]:
            count = self.riceCog[server.id][user.id]["Count"]
        else:
            count = 0

        if count != 0:
            msg = str(user.mention) + ", your warnings have been cleared!"
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            data.set_footer(text="riceBot")
            await self.bot.say(embed=data)

            count = 0
            self.riceCog[server.id][user.id].update({"Count" : count})
            dataIO.save_json(self.profile, self.riceCog)
        else:
            await self.bot.say("You don;t have any warnings to clear, " + str(user.mention) + "!")





def check_folder():
    if not os.path.exists("data/account"):
        print("Creating data/account/server.id folder")
        os.makedirs("data/account")

def check_file():
    data = {}
    f = "data/account/warnings.json"
    g = "data/account/warning_settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/account/warnings.json")
        dataIO.save_json(f, data)
    if not dataIO.is_valid_json(g):
        print("Creating data/account/warning_settings.json")
        dataIO.save_json(g, data)



def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Warn(bot))
