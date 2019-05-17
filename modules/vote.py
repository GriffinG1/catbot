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
        self.messages = []

    async def make_embed(self, ctx, arr, index):
        embed = discord.Embed(description="")
        orig_index = index
        for mod in arr:
            embed.description += f"{mod} - {unicode_letters[index]}\n"
            index += 1
        embed.set_footer(text=f"{len(self.bot.mod_dict)} total mods")
        vote_message = await ctx.send(embed=embed)
        for x in range(len(arr)):
            await vote_message.add_reaction(unicode_letters[x + orig_index])
        self.messages.append(await ctx.channel.fetch_message(vote_message.id))
        
    @commands.command()
    @commands.has_any_role("Admins")
    async def create_vote(self, ctx):
        self.messages = []
        dict = self.bot.mod_dict.copy()
        index = 0
        while len(dict) > 0:
            await self.make_embed(ctx, dict[:20], index)
            del dict[:20]
            index += 20

    @commands.command()
    async def tally(self, ctx):
        if len(self.messages) == 0:
            return await ctx.send("You need to create a vote first!")
        embed = discord.Embed(description="")
        index = 0
        for message in self.messages:
            message = await ctx.channel.fetch_message(message.id)
            for reaction in message.reactions:
                if reaction.count >= 3:
                    embed.description += f"**{self.bot.mod_dict[message.reactions.index(reaction) + index]} - {reaction.count-1}**\n"
                else:
                    embed.description += f"{self.bot.mod_dict[message.reactions.index(reaction) + index]} - {reaction.count-1}\n"
            index += 20
        await ctx.send(embed=embed)
        
    @commands.command()
    async def listopts(self, ctx):
        embed = discord.Embed(description="")
        for mod in self.bot.mod_dict:
            embed.description += f"{mod}\n"
        await ctx.send(embed=embed)

    
def setup(bot):
    bot.add_cog(Vote(bot))