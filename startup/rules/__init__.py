import nextcord
from nextcord.ext import commands
import config
from utils.embedder import embed_success
from startup.error.friendly_error import FriendlyError

class Rules(commands.Cog, name="Rules"):
    """Command for mods to update rules"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="update_rules", hidden=True)
    @commands.has_guild_permissions(administrator=True)
    async def update_rules(self, ctx: commands.Context, *, args=None):
        """Allows admins to update the embed with the rules"""
        # get the message containing the rules
        channel = self.bot.get_channel(config.RULES_CHANNEL_ID)
        message = await channel.fetch_message(config.RULES_MESSAGE_ID)
        # remove the bot command from the message
        try:
            new_rules = ctx.message.content.split(None, 1)[1]
        except ValueError as error:
            raise FriendlyError("missing content", ctx.channel, ctx.author, error)
        # update the rules
        await message.edit(
            content="",
            embed=embed_success(
                title="🚨 Gli77yGang Server Rules", description=new_rules
            ),
        )
        # confirmation
        await ctx.send(embed=embed_success("Rules have been successfully updated. 🎉"))
    
    @commands.command(name="rules", hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def rules(self, ctx):
        """SysBot Rules. with reaction role"""
        version = "v.8.4.0"

        embed = nextcord.Embed(
            title="__**Greninja SysBot Rules**__",
            description="Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
            colour=nextcord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_author(
            name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"Bot is running {version}")

        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Rules(bot))
