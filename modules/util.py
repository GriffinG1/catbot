import discord
from discord.ext import commands

class Utility(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def togglerole(self, ctx, role):
        """Toggles roles. Available: minecraft"""
        await ctx.message.delete()
        if role.lower() == "minecraft":
            if self.bot.minecraft_role in ctx.author.roles:
                await ctx.author.remove_roles(self.bot.minecraft_role)
                try:
                    await ctx.author.send("You no longer have the minecraft role.")
                except discord.Forbidden:
                    pass
            else:
                await ctx.author.add_roles(self.bot.minecraft_role)
                try:
                    await ctx.author.send("You have the minecraft role now.")
                except discord.Forbidden:
                    pass
        else:
            try:
                await ctx.author.send(f"`{role}` is not a valid entry.")
            except discord.Forbidden:
                    pass
               
    @commands.command()
    async def mentionrole(self, ctx, role):
        """Mentions a role. Available: minecraft"""
        if discord.utils.get(ctx.guild.roles, name="Admins") in ctx.author.roles or ctx.author == self.bot.creator:
            await ctx.message.delete()
            if role.lower() == "minecraft":
                await self.bot.minecraft_role.edit(mentionable=True)
                await ctx.send(f"{self.bot.minecraft_role.mention}")
                await self.bot.minecraft_role.edit(mentionable=False)
            else:
                try:
                    await ctx.author.send("`{role}` is not a valid entry.")
                except discord.Forbidden:
                        pass
        else:
            await ctx.send("You can't use this.")

    
def setup(bot):
    bot.add_cog(Utility(bot))