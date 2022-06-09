from nextcord.ext import commands
import nextcord

class EmbedModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Embed Maker",
        )
        self.emTitle =  nextcord.ui.TextInput(label = "Embed Title", min_length=2, max_length = 124, required = True, placeholder= "Enter the embed title here!")
        self.add_item(self.emTitle)
        self.emDesc =  nextcord.ui.TextInput(label = "Embed Description", min_length=5, max_length = 4000, required = True, placeholder= "Enter the embed description here!", style = nextcord.TextInputStyle.paragraph)
        self.add_item(self.emDesc)
    async def callback(self,interaction: nextcord.Interaction) -> None:
        title = self.emTitle.value
        desc = self.emDesc.value
        em = nextcord.Embed(title=title, description=desc)
        return await interaction.response.send_message(embed=em)
    
class Embed(commands.Cog, name="Embed"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="embed", description="Create a custom Embed!", guild_ids=[981781686792650822])
    async def embed(interaction: nextcord.Interaction):
        await interaction.response.send_modal(EmbedModal())

def setup(bot: commands.Bot):
    bot.add_cog(Embed(bot))