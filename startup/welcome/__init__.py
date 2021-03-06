import nextcord
from nextcord.ext import commands
import config


class WelcomeCog(commands.Cog, name="Welcome"):
    """Welcome users when they join"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """Welcome members when they join"""
        guild = self.bot.get_guild(config.GUILD_ID)
        intro_channel = guild.get_channel(config.INTRO_CHANNEL_ID)
        rules_channel = guild.get_channel(config.RULES_CHANNEL_ID)
        # don't welcome bots or members of other guilds the bot is in
        if member.bot or guild != member.guild:
            return
        # send welcome message
        await intro_channel.send(
            f"Welcome to the Gli77yGang Server, {member.mention}!\n"
            f"Please read the rules in {rules_channel.mention} to gain access to the rest of the server!"
        )
        # give the "unassigned" role
        await member.add_roles(guild.get_role(config.UNASSIGNED_ROLE_ID))

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        guild = self.bot.get_guild(config.GUILD_ID)
        outro_channel= guild.get_channel(config.INTRO_CHANNEL_ID)

        if member.bot or guild != member.guild:
            return
        
        await outro_channel.send(
            f"Peace out {member.mention}")
# setup functions for bot
def setup(bot):
    bot.add_cog(WelcomeCog(bot))