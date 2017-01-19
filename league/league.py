import discord
import aiohttp

from __main__ import send_cmd_help
from discord.ext import commands

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False

class League:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def opgg(self, ctx):
        """Shows a summoners account on OPGG"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @commands.group(pass_context = True)
    async def league(self, ctx):
        """Shows a page on http://leagueoflegends.wikia.com/"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            await self.bot.say("```\nYou have to put the ' in a if it is in a champion name.\nYou also have to capitalize champion names\n```")

    @league.command()
    async def champion(self, *, champion):
        """Finds a champion on http://leagueoflegends.wikia.com/."""
        champion = champion.title()
        champion1 = "<http://leagueoflegends.wikia.com/wiki/" + champion + ">"
        champion1 = champion1.replace("'", "%27")
        await self.bot.say(champion1.replace(" ", "_"))
        champion2 = champion.replace(" ", "")
        champion2 = champion2.replace("'", "")
        await self.bot.say("<http://champion.gg/champion/" + champion2 + ">")

    #@league.command(pass_context=True)
    #async def ability(self, ctx, *, champion):
    #    champion1 = "<http://leagueoflegends.wikia.com/wiki/" + champion + ">"
    #    champion1 = champion1.replace("'", "%27")
    #    champion1 = champion1.title() + "/Abilities"
    #    url = champion1.replace(" ", "_") #build the web adress
    #    async with aiohttp.get(url) as response:
    #        soupObject = BeautifulSoup(await response.text(), "html.parser")
    #    try:
    #        online = soupObject.find(class_='champion-icon').find('data-champion=\"{}\"').find('strong').get_text()
    #        await self.bot.say(online + ' players are playing this game at the moment')
    #    except:
    #        await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @opgg.command()
    async def na(self, *, summoner):
        await self.bot.say("http://na.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def eune(self, *, summoner):
        await self.bot.say("http://eune.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def euw(self, *, summoner):
        await self.bot.say("http://euw.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["kr"])
    async def korea(self, *, summoner):
        await self.bot.say("http://www.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["jp"])
    async def japan(self, *, summoner):
        await self.bot.say("http://jp.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["br"])
    async def brazil(self, *, summoner):
        await self.bot.say("http://br.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["tr"])
    async def turkey(self, *, summoner):
        await self.bot.say("http://tr.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["oce"])
    async def oceania(self, *, summoner):
        await self.bot.say("http://oce.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def las(self, *, summoner):
        await self.bot.say("http://las.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def lan(self, *, summoner):
        await self.bot.say("http://lan.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["ru"])
    async def russia(self, *, summoner):
        await self.bot.say("http://ru.op.gg/summoner/userName=" + summoner)



def setup(bot):
    if soupAvailable:
        bot.add_cog(League(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
