import discord
from discord.ext import commands
import logging

from cogs.defaults import default_params

class ExampleCog(commands.Cog):
    '''
    Example cog with slash commands
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command(name="info", description="Show user info", **default_params)
    @discord.option("user", type=discord.User, required=False, description="The user to get info for")
    async def info_command(self, ctx, user: discord.User = None):
        """Show user info in an embed, similar to Wick, ignoring Wick Info"""
        try:
            member = None
            if user is None:
                user = ctx.author
                member = ctx.author if hasattr(ctx, 'author') else None
            else:
                # Try to get member object for join date and roles
                member = ctx.guild.get_member(user.id) if ctx.guild else None

            embed = discord.Embed(
                title=f"Who is {user.display_name}?",
                color=member.color if member and hasattr(member, 'color') else discord.Color.default()
            )
            embed.set_thumbnail(url=user.display_avatar.url)

            # General Information
            badges = []
            if hasattr(user, 'public_flags'):
                try:
                    badges = [str(badge) if not isinstance(badge, tuple) else str(badge[0]) for badge in getattr(user.public_flags, '__iter__', lambda:[])() if badge]
                except Exception:
                    badges = []
            embed.add_field(
                name="General Informations:",
                value=(
                    f"**Name:** {user.mention}\n"
                    f"**ID:** {user.id}\n"
                    f"**Creation:** {discord.utils.format_dt(user.created_at, 'R')}\n"
                    f"**Join:** {discord.utils.format_dt(member.joined_at, 'R') if member and member.joined_at else 'Unknown'}\n"
                    f"**Color:** {str(member.color) if member and hasattr(member, 'color') else '#000000'}\n"
                    f"**Discord Badges:** {' '.join(badges) if badges else 'None'}"
                ),
                inline=False
            )

            # Account Accessories
            roles = []
            if member:
                roles = [role.mention for role in member.roles if role.name != "@everyone"]
            embed.add_field(
                name="Account Accessories:",
                value=(
                    f"**Roles:** {' '.join(roles) if roles else 'None'}\n"
                    f"**Webhooks:** ❌"
                ),
                inline=False
            )

            await ctx.respond(embed=embed)
        except Exception as e:
            logging.error(f"Error in info command: {e}")
            await ctx.respond("An error occurred while processing your command.")

def setup(bot: discord.Bot) -> None:
    """Add the cog to the bot"""
    bot.add_cog(ExampleCog(bot)) 