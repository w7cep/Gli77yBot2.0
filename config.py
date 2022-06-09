import os
from dotenv.main import load_dotenv

load_dotenv()

# Bot setup
PREFIX = "!"
BOT_NAME = "Gli77yBot"
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Discord Guild ID
GUILD_ID = int(os.getenv("GUILD_ID"))

# Discord Channel IDs
INTRO_CHANNEL_ID = int(os.getenv("INTRO_CHANNEL_ID"))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID"))
BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID"))


# Discord Role IDs
VIP_ROLE_ID = int(os.getenv("VIP_ROLE_ID"))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID"))
UNASSIGNED_ROLE_ID = int(os.getenv("UNASSIGNED_ROLE_ID"))
RD_ROLE_ID = int(os.getenv("RD_ROLE_ID"))

# Discord Message IDs
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID"))


