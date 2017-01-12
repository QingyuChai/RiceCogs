"""Warning cog"""
import discord
import os
import shutil

from .utils.chat_formatting import *
from .utils.dataIO import fileIO
from .utils import checks
from discord.ext import commands 
from enum import Enum
import aiohttp
import asyncio

class Warn:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.is_owner()
    async def wipe(self, ctx, *, content):
        """Wipes warnings in general or for a certain server"""
        author = ctx.message.author
        server = author.server
        if content == "server":
            if os.path.exists("data/warning/" + str(server)):
                shutil.rmtree("data/warning/" + str(server))
                await self.bot.say("Warnings wiped from " + str(server) + "!")
            else:
                await self.bot.say("There have been no warnings on this server")
        else:
            try:
                if os.path.exists("data/warning/" + str(content)):
                    shutil.rmtree("data/warning/" + str(content))
                    await self.bot.say("Warnings wiped from " + str(content) + "!")
                else:
                    await self.bot.say("There have been no warnings on this server")
            except Exception as e:
                print (e)
                await self.bot.say(e)




    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    async def clean(self, ctx, user : discord.Member):
        """Removes warnings from a user"""
        colour = '099999'
        author = ctx.message.author
        server = author.server
        count = ["/first", "/second", "/third"]
        if os.path.exists("data/warning/"+ str(server) + "/" + str(user.id) + "/first"):
            #msg = "```\n"
            msg = "Warning(s) succesfully removed."
            #msg += "\n```"
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            data.set_footer(text="Bananya")
            await self.bot.say(embed=data)
        else:
            #msg = "```\n"
            msg = "User had no previous warning(s)."
            #msg += "\n```"
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            data.set_footer(text="Bananya")
            await self.bot.say(embed=data)
        for warning in count:
            if os.path.exists("data/warning/" + str(server) + "/" + str(user.id) + warning):
                os.rmdir("data/warning/" + str(server) + "/" + str(user.id) + warning)
        os.rmdir("data/warning/" + str(server) + "/" + str(user.id))





    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    async def warn(self, ctx, user : discord.Member):
        """Warns the user, after 3 warnings user gets kicked"""
        colour = '099999'
        author = ctx.message.author
        server = author.server
        if not os.path.exists("data/warning/" + str(server) + "/" + str(user.id)):
            os.makedirs("data/warning/" + str(server) + "/" + str(user.id))
            os.makedirs("data/warning/" + str(server) + "/" + str(user.id) + "/first")
            msg = str(user.mention) + ", you have received your first warning! At three warnings you will be **kicked**!"
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            data.set_footer(text="Bananya")
            await self.bot.say(embed=data)
        elif os.path.exists("data/warning/" + str(server) + "/" + str(user.id) + "/first") and not os.path.exists("data/warning/" + str(server) + "/" + str(user.id) + "/second"):
            os.makedirs("data/warning/" + str(server) + "/"+ str(user.id) + "/second")
            msg = str(user.mention) + ", you have received your second warning! One more warning and you will be **kicked**!"
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name="Warning", value=msg)
            data.set_footer(text="Bananya")
            await self.bot.say(embed=data)        
        elif os.path.exists("data/warning/" + str(server) + "/" + str(user.id) + "/second"):
            os.makedirs("data/warning/" + str(server) + "/" + str(user.id) + "/third")
            os.rmdir("data/warning/" + str(server) + "/" + str(user.id) + "/first")
            os.rmdir("data/warning/" + str(server) + "/" + str(user.id) + "/second")
            os.rmdir("data/warning/" + str(server) + "/" + str(user.id) + "/third")
            os.rmdir("data/warning/" + str(server) + "/" + str(user.id))
            try:
                msg = str(user.name) + " has been **kicked** after 3 warnings."
                data = discord.Embed(colour=discord.Colour(value=colour))
                data.add_field(name="Warning", value=msg)
                data.set_footer(text="Bananya")
                await self.bot.say(embed=data)
                await self.bot.kick(user)
                logger.info("{}({}) kicked {}({})".format(
                    author.name, author.id, user.name, user.id))
                await self.new_case(str(server),
                                    action="Kick \N{WOMANS BOOTS}",
                                    mod=author,
                                    user=user)
                await self.bot.say("Done. That felt good.")
            except discord.errors.Forbidden:
                await self.bot.say("I'm not allowed to do that.")
            except Exception as e:
                print(e)



 
def setup(bot):
    bot.add_cog(Warn(bot))