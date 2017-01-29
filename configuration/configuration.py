import discord
import os

from .utils.dataIO import fileIO, dataIO
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.chat_formatting import pagify


class Config:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/servers/serverlist.json"
        self.riceCog = dataIO.load_json(self.profile)
        self.down_message = "data/servers/down_message.json"
        self.down = dataIO.load_json(self.down_message)

    async def _message_servers(self, ctx, msg):
        for server in self.bot.servers:
            if server.id in self.riceCog:
                try:
                    channel_id  = self.riceCog[server.id]["Channel"]
                    channel = self.bot.get_channel(channel_id)
                    await self.bot.send_message(channel, msg)
                except:
                    pass
            else:
                try:
                    await self.bot.send_message(server, msg)
                except:
                    pass
        await self.bot.say("Message succesfully sent")

    @checks.admin_or_permissions(manage_server=True)
    @commands.command(pass_context=True)
    async def channelset(self, ctx, channel : discord.Channel):
        """Set channel where announcements arrive"""
        server = ctx.message.server
        if server.id in self.riceCog:
            pass
        else:
            self.riceCog[server.id] = {}
        self.riceCog[server.id].update({"Channel" : channel.id})
        dataIO.save_json(self.profile, self.riceCog)
        await self.bot.say("Succesfully changed the channel to get notifications in.")


    @commands.command()
    async def countservers(self):
        """
        Checks how many servers the bot is on"""
        msg = "The bot is in **"
        msg += str(len(self.bot.servers))
        msg += "** servers."
        await self.bot.say(msg)

    @commands.command()
    @checks.is_owner()
    async def shout(self, server_id, channel_id, *, message):
        """
        Shouts a message to the main channel of a certain server"""
        msg = "```asciidoc\n"
        msg += "Announcement :: Information\n"
        msg += message
        msg += "\n```"

        if channel_id == "main":
            channel_id = None
            channel = None
        else:
            channel = discord.utils.get(self.bot.get_all_channels(), id=channel_id)

        for server in self.bot.servers:
            if server.id == server_id:
                if channel in server.channels:
                    try:
                        await self.bot.send_message(channel, msg)
                        await self.bot.say("'{}' has been sent to {} in {}.".format(message, channel.name, channel.server))
                    except discord.errors.Forbidden:
                        await self.bot.say("I'm not allowed to do that.")
                else:
                    try:
                        await self.bot.send_message(server, msg)
                        await self.bot.say("Couldn't find channel with id {}, so I just sent the message to the main channel instead.".format(channel_id))
                    except discord.errors.Forbidden:
                        await self.bot.say("I'm not allowed to do that.")

    @commands.command()
    @checks.is_owner()
    async def listchannels(self, server_id):
        """
        Checks what text channels are in a server"""
        server = self.bot.get_server(server_id)
        msg = "```asciidoc\n"
        # msg += "\n"
        count = 0
        for channel in server.channels:
            if channel.type != "voice":
                channelname = channel.name.replace("_", "-")
                msg += "{} :: {}\n".format(channel.id, channelname)
                count += 1
        await self.bot.say("The server {} has {} text channels:".format(server.name, count))
        await self.bot.say(msg + "```")

    @commands.command()
    @checks.is_owner()
    async def listservers(self):
        """
        Checks what servers the bot is on"""
        servers = self.bot.servers
        await self.bot.say("```asciidoc\nThe bot is in the following {} server(s):\n```".format(str(len(self.bot.servers))))
        msg = "```asciidoc\n"
        msg2 = "```asciidoc\n"
        msg3 = "```asciidoc\n"
        msg4 = "```asciidoc\n"
        # msg += "\n"

        messages = [msg, msg2, msg3, msg4]
        count = 0
        for server in servers:
            if len(server.members) < 10:
                messages[count] += "{:<1} :: 000{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members) < 100:
                messages[count] += "{:<1} :: 00{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members) < 1000:
                messages[count] += "{:<1} :: 0{} users :: {}".format(server.id, len(server.members), server.name)
            else:
                messages[count] += "{:<1} :: {} users :: {}".format(server.id, len(server.members), server.name)
            messages[count] += "\n"
            if len(messages[count]) > 1500:
                count = count + 1

        for message in messages:
            if len(message) > 30:
                await self.bot.say(message + "\n```")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def discrim(self, ctx, discriminator):
        """
        Find users with this discriminator"""
        msg = "Users with discriminator " + discriminator
        msg += ": \n"
        for r in self.bot.get_all_members():
            if r.discriminator == discriminator:
                if r.name in msg:
                    pass
                else:
                    msg += "```\n"
                    msg += r.name
                    msg += "\n```"
        await self.bot.say(msg)

    @commands.command()
    async def countusers(self):
        """
        Checks how many users the bot is connected to"""
        msg = "The bot is connected to **"
        msg += str(len(set(self.bot.get_all_members())))
        msg += "** users."
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def notify(self, ctx, *, content):
        """Notifies every server"""
        prefix = ctx.prefix
        if content == "info":
            msg = "```asciidoc\n"
            msg += "Announcement :: Information\n"
            msg += "= -=-=-=-=-=-=-=-=-=-=-=- =\n"
            msg += "Thank you for inviting riceBot!\n"
            msg += "For basic information on the bot, a list of commands, or to contact the owner, use: \n"
            msg += "= {}rice =\n".format(prefix)
            msg += "= {}help =\n".format(prefix)
            msg += "= {}contact =\n".format(prefix)
            msg += "To add the bot to your own server, open this:: https://discordsites.com/ricebot/\n"
            msg += "= -=-=-=-=-=-=-=-=-=-=-=- =\n"
            msg += "riceBot ~ managed by FwiedWice"
            msg += "\n```"
        else:
            msg = "```asciidoc\n"
            msg += "Announcement :: Information\n"
            msg += content
            msg += "\n```"
        await self._message_servers(ctx, msg)

    #def __shutdown(self):
    #   """Credits to Kowlin for this"""
    #    self.bot.loop.create_task(self.task())

    #async def task(self):
    #    msg = ("```asciidoc\n"
    #           "Announcement :: Shutdown\n"
    #           "riceBot shutting down... Will be up again soon!"
    #           "\n```")
    #    for server in self.bot.servers:
    #        try:
    #            await self.bot.send_message(server, msg)
    #        except:
    #            pass
    #    await self.bot.say("asdasd")

    #Credits to Kowlin for formatting!
    @commands.command(pass_context=True)
    @checks.is_owner()
    async def setshutdownmsg(self, ctx, *, msg : str=None):
        """Sets the shutdown message"""
        if msg == None:
            msg = ("```asciidoc\n"
                   "Announcement :: Shutdown\n"
                   "riceBot shutting down... Will be up again soon!"
                   "\n```")
        await self.bot.say("The shutdown message is: ")
        await self.bot.say(msg)
        self.down.update({"Message" : msg})
        dataIO.save_json(self.down_message, self.down)


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def shutdown(self, ctx, silently : bool=False):
        """Shuts down riceBot"""
        if "Message" in self.down:
            msg = self.down["Message"]
        else:
            msg = ("```asciidoc\n"
                   "Announcement :: Shutdown\n"
                   "riceBot shutting down... Will be up again soon!"
                   "\n```")
        await self._message_servers(ctx, msg)
        try: # We don't want missing perms to stop our shutdown
            if not silently:
                await self.bot.say("Shutting down... ")
        except:
            pass
        await self.bot.shutdown()

    @commands.command()
    @checks.is_owner()
    async def speak(self, *, content):
        """Says something"""
        await self.bot.say(content)


def check_folder():
    if not os.path.exists("data/servers"):
        print("Creating data/servers folder")
        os.makedirs("data/servers")

def check_file():
    data = {}
    f = "data/servers/serverlist.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/servers/serverlist.json")
        dataIO.save_json(f, data)

def check_file1():
    data = {}
    f = "data/servers/down_message.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/servers/down_message.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    check_file1()
    bot.remove_command('shutdown')
    bot.add_cog(Config(bot))
