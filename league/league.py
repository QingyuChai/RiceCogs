import discord
import aiohttp
import json
try:
    from cassiopeia import riotapi
    isAvailable = True
except Exception as e:
    print(e)
    isAvailable = False

key = ''  #input key for now
riotapi.set_api_key(key) #keycheck
#command to set key


from __main__ import send_cmd_help
from discord.ext import commands


class League:
    def __init__(self, bot):
        self.bot = bot
        riotapi.set_region("eune")

    @commands.group(pass_context = True)
    async def opgg(self, ctx):
        """Shows a summoners account on OPGG"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @commands.command(pass_context = True)
    async def lastmatch(self, ctx, region, *, summoner):
        try:
            riotapi.set_region(region)
        except ValueError as e:
            print(e)
            await self.bot.say("Invalid region! Try again.")
            return
        except Exception as e:
            print(e)
            await self.bot.say("Check your console for logs.")
            return
        try:
            summoner = riotapi.get_summoner_by_name(summoner)
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid summoner. Either wrong "
                               "summoner name or region. Check your console.")
            return

        name = summoner.name
        _id = summoner.id
        region = region
        level = summoner.level
        matches = summoner.recent_games()
        last_match = matches[0].to_json()
        last_match = json.loads(last_match)
        match_type = last_match['subType'].title()
        deaths = last_match['stats']["numDeaths"]
        kills = last_match['stats']['championsKilled']
        assists = last_match['stats']['assists']
        last_champion_id = last_match['championId']
        last_champion_name = riotapi.get_champion_by_id(last_champion_id).name
        creeps = last_match['stats']["minionsKilled"]
        poop = True
        try:
            triple_kills = last_match['tripleKills']
            triple = True
        except:
            triple = False
        try:
            quadra_kills = last_match['quadraKills']
            quadra = True
        except:
            quadra = False
        try:
            penta_kills = last_match['pentaKills']
            penta = True
        except:
            penta = False
        msg =  "```ruby\n"
        msg += "Last Match of {}:\n\n".format(name)
        msg += "Match Type     -   {}\n".format(match_type)
        msg += "Region         -   {}\n".format(region.upper())
        msg += "Champion       -   {}\n".format(last_champion_name)
        msg += "Score K/D/A    -   {}/{}/{}\n".format(kills, deaths, assists)
        msg += "Creep Score    -   {}".format(creeps)
        if triple:
            msg += "Triple Kills   -   {}".format(triple_kills)
        if quadra:
            msg += "Quadra Kills   -   {}".format(quadra_kills)
        if penta:
            msg += "Penta Kills    -   {}".format(penta_kills)

        msg += "```"
        await self.bot.say(msg)

    @commands.command(pass_context = True)
    async def summoner(self, ctx, region, *, summoner):
        try:
            riotapi.set_region(region)
        except ValueError as e:
            print(e)
            await self.bot.say("Invalid region! Try again.")
            return
        except Exception as e:
            print(e)
            await self.bot.say("Check your console for logs.")
            return
        try:
            summoner = riotapi.get_summoner_by_name(summoner)
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid summoner. Either wrong "
                               "summoner name or region. Check your console.")
            return

        name = summoner.name
        _id = summoner.id
        region = region
        level = summoner.level
        ma_pages = len(summoner.mastery_pages())
        ru_pages = len(summoner.rune_pages())


        msg =  "```ruby\n"
        msg += "Who is {}:\n\n".format(name)
        msg += "Summoner Name  -   {}\n".format(name)
        msg += "Summoner ID    -   {}\n".format(_id)
        msg += "Summoner Lvl   -   {}\n".format(level)
        msg += "Mastery Pages  -   {}\n".format(str(ma_pages))
        msg += "Rune Pages     -   {}\n".format(str(ru_pages))
        msg += "```"
        await self.bot.say(msg)

    @commands.command(pass_context = True)
    async def champion(self, ctx, *, champion):
        champion = champion.title()
        try:
            champ = riotapi.get_champion_by_name(champion)
            champ.name
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid champion. Either wrong "
                               "name or error. Check your console.")
            return
        name = champ.name
        _id = champ.id

        q = ""
        w = ""
        e = ""
        r = ""

        p = champ.passive.name

        abilities = [q, w, e ,r]
        spells = ["Q", "W", "E", "R"]
        i = 0
        while i <= 3:
            abilities[i] = champ.spells[i].name
            i += 1
        msg =  "```ruby\n"
        msg += "Who is {}:\n\n".format(name)
        msg += "Champion Name  -   {}\n".format(name)
        msg += "Champion ID    -   {}\n".format(_id)
        msg += "Passive        -   {}\n".format(p)
        i = 0
        while i <= 3:
            ability = abilities[i]
            spell = spells[i]
            msg += "{}              -   {}\n".format(spell, ability)
            i += 1
        msg += "```"
        await self.bot.say(msg)












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
    if isAvailable:
        bot.add_cog(League(bot))
    else:
        raise RuntimeError("You need to run `pip3 install cassiopeia`")
