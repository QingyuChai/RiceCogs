"""Use Caesar shift to encode or decode your messages!"""

import os

import discord
from .utils.dataIO import fileIO, dataIO
from discord.ext import commands
from __main__ import send_cmd_help
from .utils import checks


__author__ = "FwiedWice"
__version__ = "V1.0.0"

class Code:
    def __init__(self, chars):
        self.chars = list(chars)

    async def code(self, number, en_or_de, text):

        to_process = list(text)
        length = len(self.chars)
        i = 0
        result = []
        if en_or_de == "de":
            number = 0 - number

        while i < len(to_process):
            if to_process[i].lower() in self.chars:
                index = self.chars.index(to_process[i].lower())
                index += number
                if index < 0:
                    index += length
                if index >= length:
                    index -= length

                letter = self.chars[index]
                if to_process[i].lower() != to_process[i]:
                    letter = letter.upper()
                result.append(letter)
            else:
                result.append(to_process[i])
            i += 1
        return "".join(result)

class Cypher:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/cypher/charset.json"
        self.riceCog = dataIO.load_json(self.profile)
        self.chars = "abcdefghijklmnopqrstuvwxyz"

    @commands.group(pass_context=True)
    async def cypher(self, ctx):
        if not ctx.invoked_subcommand:
            await send_cmd_help(ctx)

    @checks.admin_or_permissions(manage_server=True)
    @cypher.command(pass_context=True)
    async def delmsg(self, ctx):
        """Toggle whether to delete the message that needs to
        be encoded/decoded"""

        server = ctx.message.server
        do_del = True

        if server.id not in self.riceCog:
            self.riceCog[server.id] = {}

        if 'del' in self.riceCog[server.id]:
            do_del = self.riceCog[server.id]['del']

        do_del = not do_del

        self.riceCog[server.id]['del'] = do_del
        dataIO.save_json(self.profile, self.riceCog)

        if do_del:
            await self.bot.say("Message will be deleted.")
        else:
            await self.bot.say("Message will not be deleted.")

    @checks.admin_or_permissions(manage_server=True)
    @cypher.command(pass_context=True)
    async def reset(self, ctx, chars = None):
        """Reset server settings"""

        server = ctx.message.server
        if server.id in self.riceCog:
            del self.riceCog[server.id]
        dataIO.save_json(self.profile, self.riceCog)
        await self.bot.say("Server settings deleted.")

    @checks.admin_or_permissions(manage_server=True)
    @cypher.command(pass_context=True)
    async def setchar(self, ctx, chars = None):
        """Set character set for [p]encode/decode commands"""

        server = ctx.message.server

        if not chars:
            msg = ("```Set a character set. Example:\n\n"
                   "*abcdefghijklmnopqrstuvwxyz*\n\n Those will be the "
                   "characters that [p]encode/decode will work with.")
            await self.bot.say(msg)
            return
        if len(chars) > 100:
            await self.bot.say("```Hold up a second... you don't need more than"
                               " 100 characters.```")
            return
        if server.id not in self.riceCog:
            self.riceCog[server.id] = {}

        self.riceCog[server.id]['charset'] = chars
        dataIO.save_json(self.profile, self.riceCog)
        await self.bot.say("```The character set is now:\n\n*{}*```".format(chars))

    @commands.command(pass_context=True)
    async def encode(self, ctx, how_much : int, *, message):
        """Encode a message!
        how_much is the amount you want to shift/encode your message by.
        """

        server = ctx.message.server
        channel = ctx.message.channel

        chars = self.chars
        do_del = False

        if server.id in self.riceCog:
            if 'charset' in self.riceCog[server.id]:
                chars = self.riceCog[server.id]['charset']
            if 'del' in self.riceCog[server.id]:
                do_del = self.riceCog[server.id]['del']

        if do_del:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.errors.Forbidden:
                await self.bot.say("Tried to delete the message but can't! \n"
                                   "Lacking permissions.")

        tool = Code(chars)

        result = await tool.code(how_much, 'en', message)
        await self.bot.say("```You're encoded message is:\n\n{}```".format(result))

    @commands.command(pass_context=True)
    async def decode(self, ctx, how_much : int, *, message):
        """Decode a message!
        how_much is the amount you want to shift/decode your message by.
        """

        server = ctx.message.server
        channel = ctx.message.channel

        chars = self.chars
        do_del = False

        if server.id in self.riceCog:
            if 'chars' in self.riceCog[server.id]:
                chars = self.riceCog[server.id]['charset']
            if 'del' in self.riceCog[server.id]:
                do_del = self.riceCog[server.id]['del']

        if do_del:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.errors.Forbidden:
                await self.bot.say("Tried to delete the message but can't! \n"
                                   "Lacking permissions.")

        tool = Code(chars)

        result = await tool.code(how_much, 'de', message)
        await self.bot.say("```You're decoded message is:\n\n{}```".format(result))

def check_folder():
    if not os.path.exists("data/cypher"):
        print("Creating data/cypher/server.id folder")
        os.makedirs("data/cypher")

def check_file():
    data = {}
    f = "data/cypher/charset.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/cypher/charset.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Cypher(bot))
