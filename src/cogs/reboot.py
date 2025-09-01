import discord
from discord.ext import commands
import os
import sys

class RebootCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="reboot", description="Reboot the bot (owner only)")
    async def reboot(self, ctx):
        app_info = await self.bot.application_info()
        if ctx.author.id != app_info.owner.id:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
            return
        await ctx.respond("Rebooting...", ephemeral=True)
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)

def setup(bot):
    bot.add_cog(RebootCog(bot)) 