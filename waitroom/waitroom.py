import discord
import logging
import os

from .utils import checks
from .utils.dataIO import dataIO
from discord.ext import commands

class Waitroom:
    """"""

    def __init__(self, bot):
        self.bot = bot
        self.waitroom = "data/waitroom/waitroom.json"
        self.riceCog = dataIO.load_json(self.waitroom)
        self.defaultrole = "data/waitroom/defaultrole.json"
        self.roleset = dataIO.load_json(self.defaultrole)


    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def setwaitroom(self, ctx, channel : discord.Channel):
        server = ctx.message.server
        if server.id not in self.riceCog:
            self.riceCog[server.id] = channel.id
            dataIO.save_json(self.waitroom, self.riceCog)
        else:
            self.riceCog[server.id] = channel.id
            dataIO.save_json(self.waitroom, self.riceCog)
        await self.bot.say("Succesfully changed the *Waitroom* channel to {}".format(channel.name))


    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def setdefaultrole(self, ctx, default_role):
        server = ctx.message.server
        count = 0
        for role in server.roles:
            if role.name.lower() == default_role.lower():
                default_role = role
                break
            else:
                count += 1

        if count == len(server.roles):
            await self.bot.say("Role does not exist on this server. Please try again.")
            return
        if server.id not in self.roleset:
            self.roleset[server.id] = default_role.id
            dataIO.save_json(self.defaultrole, self.roleset)
        else:
            self.roleset[server.id] = default_role.id
            dataIO.save_json(self.defaultrole, self.roleset)
        await self.bot.say("Succesfully changed the default *role* to {}!".format(default_role))

    @commands.command(pass_context=True)
    async def register(self, ctx):
        author = ctx.message.author
        server = author.server
        channel = ctx.message.channel
        user = author
        prefix = ctx.prefix
        if server.id in self.riceCog and server.id in self.roleset:
            default_role = self.roleset[server.id]
            await self.bot.say("Type **agreed** to get access to the server.")
            msg = await self.bot.wait_for_message(author=author, channel=channel)
            if msg.content.lower().strip() == "agreed":
                try:
                    for role in server.roles:
                        if role.id == default_role:
                            userrole = role
                            break
                    await self.bot.add_roles(author, userrole)
                    await self.bot.say("Congratulations!")
                except discord.errors.Forbidden:
                    await self.bot.say("Try checking bot permissions!")
                except:
                    await self.bot.say("Try checking the role again!")
            else:
                await self.bot.say("Try again!")
        else:
            await self.bot.say("You did not set the *Waitroom* channel yet! To do so, do {}setwaitroom [channel]!".format(prefix))
            await self.bot.say("Also, set the default role using {}setdefaultrole [rolename]!".format(prefix))


def check_folder():
    if not os.path.exists("data/waitroom"):
        print("Creating data/waitroom folder")
        os.makedirs("data/waitroom")

def check_file():
    data = {}
    f = "data/waitroom/waitroom.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/waitroom/waitroom.json")
        dataIO.save_json(f, data)

def check_file1():
    data = {}
    f = "data/waitroom/defaultrole.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/waitroom/defaultrole.json")
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    check_file1()
    bot.add_cog(Waitroom(bot))
