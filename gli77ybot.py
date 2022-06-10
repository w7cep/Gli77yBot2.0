import os
import aiohttp
import nextcord
from nextcord.ext import commands
import aiosqlite
import config
import asyncio
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print("~~~~~~~~~~~\n\n")
print(f"Current Working Directory:\n{cwd}\n")

async def getprefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
            data = await cursor.fetchone()
            if data:
                return data
            else:
                return "!"

def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    intents = nextcord.Intents.all()
    intents.guilds = True
    intents.members = True

    activity = nextcord.Activity(
        type=nextcord.ActivityType.listening, name="!help"
    )

    bot = commands.Bot(
        command_prefix=getprefix,
        intents=intents,
        activity=activity,
        owner_id=config.OWNER_ID,
    )

    # boolean that will be set to true when views are added
    bot.persistent_views_added = False


    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord.")
        setattr(bot, "db", await aiosqlite.connect("main.db"))
        await asyncio.sleep(3)
        async with bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT , guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER , guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS levelSettings (levelsys BOOL, role INTEGER, levelreq INTEGER, guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS starSetup (starLimit INTEGER, channel INTEGER, guild INTEGER)")
        await bot.db.commit()

      # load all cogs
    for folder in os.listdir("startup"):
        bot.load_extension(f"startup.{folder}")

    async def startup():
        bot.session = aiohttp.ClientSession()

    bot.loop.create_task(startup())

    # run the bot
    bot.run(config.BOT_TOKEN)


if __name__ == "__main__":
    main()