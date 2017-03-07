import discord
import os
import collections
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/help/toggle.json"
        self.riceCog = dataIO.load_json(self.profile)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def sethelp(self, ctx):
        self.profile = "data/help/toggle.json"
        self.riceCog = dataIO.load_json(self.profile)
        dm_msg = "The help message will now be send in DM."
        no_dm_msg = "The help message will now be send into the channel."
        if 'toggle' not in self.riceCog:
            self.riceCog['toggle'] = "no_dm"
            dataIO.save_json(self.profile, self.riceCog)
            msg = no_dm_msg
        elif self.riceCog['toggle'] == "dm":
            self.riceCog['toggle'] = "no_dm"
            dataIO.save_json(self.profile, self.riceCog)
            msg = no_dm_msg
        elif self.riceCog['toggle'] == "no_dm":
            self.riceCog['toggle'] = "dm"
            dataIO.save_json(self.profile, self.riceCog)
            msg = dm_msg
        if msg:
            await self.bot.say(msg)



    @commands.command(name='help', pass_context=True)
    async def _help(self, ctx, command = None):
        if 'toggle' not in self.riceCog:
            self.riceCog['toggle'] = "dm"
            dataIO.save_json(self.profile, self.riceCog)
            await self.bot.say("Help message is set to DM by default. use "
                               "**{}sethelp** to change it!".format(ctx.prefix))
            toggle = self.riceCog['toggle']
        else:
            toggle = self.riceCog['toggle']
        if not command:
            msg = "**Command list:**"
            color = 0xffa500

            em=discord.Embed(description=msg, color=color)

        #await self.bot.say("Hello.")
        #await self.bot.say(coms)
            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if self.bot.commands[com].module.__name__ not in com_groups:
                        com_groups.append(self.bot.commands[com].module.__name__)
                    else:
                        continue
                except Exception as e:
                        print(e)
                        print(datetime.datetime.now())
                        continue
            com_groups.sort()
            alias = []
            #print(com_groups)
            for com_group in com_groups:
                commands = []
                for com in self.bot.commands:
                    if com in self.bot.commands[com].aliases:
                        continue
                    if com_group == self.bot.commands[com].module.__name__:
                    #print("PLS WURK")
                        #if self.bot.commands[com].aliases == alias:
                        commands.append(com)
                final_coms[com_group] = commands

            #print(commands)
        #print(final_coms)

            final_coms = collections.OrderedDict(sorted(final_coms.items()))
            #print(final_coms)

            for group in final_coms:
                #width = len(max(words, key=len))
                msg = ""
                final_coms[group].sort()
                count = 0
                for com in final_coms[group]:
                #drugs = self.bot.commands[com].help
                #if not drugs:
                    #drugs = "No description available."
                #msg += '```md\n'
                    if count == 0:
                        msg += '`{}`'.format(com)
                    else:
                        msg += '~`{}`'.format(com)
                    count += 1
                #msg += '```'
                #msg += '    {}\n'.format(str(drugs))
                cog_name = group.replace("cogs.", "").title()
                cog =  "```\n"
                cog += cog_name
                cog += "\n```"
                em.add_field(name=cog, value=msg, inline=False)


            if toggle == "dm":
                await self.bot.say("Hey there, {}! I sent you a list of commands"
                                   " through DM.".format(ctx.message.author.mention))
                await self.bot.send_message(ctx.message.author, embed=em)
                await self.bot.send_message(ctx.message.author,
                                        "An instance of Red - DiscordBot, made "
                                        "by Twentysix26 and improved by many.")
            elif toggle == 'no_dm':
                await self.bot.say(embed=em)
                await self.bot.say("An instance of Red - DiscordBot, "
                                   "made by Twentysix26 and improved by many.")

        else:
            msg = "**Command Help:**"
            color = 0x002B36

            em=discord.Embed(description=msg, color=color)
            try:
                commie =  "```\n"
                commie += command
                commie += "\n```"
                info = self.bot.commands[command].help
                em.add_field(name=commie, value=info, inline=False)
                await self.bot.say(embed=em)
            except Exception as e:
                print(e)
                await self.bot.say("Couldn't find command! Try again.")

def check_folder():
    if not os.path.exists("data/help"):
        print("Creating data/help folder")
        os.makedirs("data/help")

def check_file():
    data = {}
    f = "data/help/toggle.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/help/toggle.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.remove_command('help')
    bot.add_cog(Help(bot))
