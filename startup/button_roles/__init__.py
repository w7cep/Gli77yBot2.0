import config
import nextcord
from nextcord.ext import commands
from .confirm_view import ConfirmView
from .self_role_view import SelfRoleView
from .vip_view import VIPView


class ButtonRolesCog(commands.Cog, name="Button Roles"):
    """Give and remove roles based on button presses"""

    def __init__(self, bot: commands.Bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready, load the role views"""
        # skip this function if views are already added
        if self.__bot.persistent_views_added:
            return
        self.__bot.add_view(SelfRoleView())
        self.__bot.add_view(ConfirmView())
        self.__bot.add_view(VIPView())
        # set flag
        self.__bot.persistent_views_added = True
        print("Button views added")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def roles(self, ctx: commands.Context):
        """Starts a role view"""
        await ctx.send("Click a button to add or remove a role.", view=SelfRoleView())

    @commands.command(hidden=True)
    @commands.is_owner()
    async def VIP(self, ctx: commands.Context):
        """VIP"""
        version = "v.8.4.0"

        embed = nextcord.Embed(
            title="__**VIP Access**__",
            description="Gain access to VIP treatment!",
            colour=nextcord.Colour.blue()
        )
        """embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_author(
            name="Gli77yBot", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")"""
        embed.set_footer(text=f"Bot is running {version}")
        
        await ctx.send(embed=embed, view=VIPView())

    @commands.command(hidden=True)
    @commands.is_owner()
    async def add_confirm(self, ctx: commands.Context, message_id: str):
        """Starts a confirm view"""
        rules_channel = await ctx.guild.fetch_channel(config.RULES_CHANNEL_ID)
        message = await rules_channel.fetch_message(message_id)
        await message.edit(view=ConfirmView())


# setup functions for bot
def setup(bot):
    bot.add_cog(ButtonRolesCog(bot))
