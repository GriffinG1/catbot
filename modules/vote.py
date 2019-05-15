import discord
from discord.ext import commands

unicode_letters = [
    "🇦",
    "🇧",
    "🇨",
    "🇩",
    "🇪",
    "🇫",
    "🇬",
    "🇭",
    "🇮",
    "🇯",
    "🇰",
    "🇱",
    "🇲",
    "🇳",
    "🇴",
    "🇵",
    "🇶",
    "🇷",
    "🇸",
    "🇹",
    "🇺",
    "🇻",
    "🇼",
    "🇽",
    "🇾",
    "🇿",
    "0\N{combining enclosing keycap}",
    "1\N{combining enclosing keycap}",
    "2\N{combining enclosing keycap}",
    "3\N{combining enclosing keycap}",
    "4\N{combining enclosing keycap}",
    "5\N{combining enclosing keycap}",
    "6\N{combining enclosing keycap}",
    "7\N{combining enclosing keycap}",
    "8\N{combining enclosing keycap}",
    "9\N{combining enclosing keycap}",
    "🔟"
]

class Vote(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def make_embed(self, ctx, arr, index):
        embed = discord.Embed(description="")
        orig_index = index
        for mod in arr:
            embed.description += f"{mod[0]} - {unicode_letters[index]}\n"
            index += 1
        embed.set_footer(text=f"{len(self.bot.mod_dict)} total mods")
        vote_message = await ctx.send(embed=embed)
        for x in range(len(arr)):
            await vote_message.add_reaction(unicode_letters[x + orig_index])
        
    @commands.command()
    async def create_vote(self, ctx):
        dict = self.bot.mod_dict.copy()
        index = 0
        while len(dict) > 0:
            await self.make_embed(ctx, dict[:20], index)
            del dict[:20]
            index += 20

    
def setup(bot):
    bot.add_cog(Vote(bot))