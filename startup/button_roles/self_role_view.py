from startup.button_roles.role_view import RoleView
from utils.utils import custom_id
import nextcord
import config

VIEW_NAME = "SelfRoleView"


class SelfRoleView(RoleView):
    def __init__(self):
        super().__init__(required_roles=[config.MEMBER_ROLE_ID])

    @nextcord.ui.button(
        label="R&D",
        emoji="🥼",
        style=nextcord.ButtonStyle.primary,
        custom_id=custom_id(VIEW_NAME, config.RD_ROLE_ID),
    )
    async def RD_button(self, button, interaction):
        await self.handle_click(button, interaction)
   