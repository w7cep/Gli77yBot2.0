import nextcord
from nextcord.ext import commands
import os

class Utility(commands.Cog, name="Utility"):
    """Bot Utility"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", ("!", guild.id,))
            await self.bot.db.commit()
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM prefixes WHERE guild = ?", (guild.id,))
            await self.bot.db.commit()

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def config(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()

    @config.command(aliases=['game'])
    @commands.has_role('Bot Manager')
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Changes the game currently playing (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            activityType = nextcord.ActivityType.playing
        elif gameType == 'watching':
            activityType = nextcord.ActivityType.watching
        elif gameType == 'listening':
            activityType = nextcord.ActivityType.listening
        elif gameType == 'streaming':
            activityType = nextcord.ActivityType.streaming
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(activity=nextcord.Activity(type=activityType, name=gameName))
        await ctx.send(f'**:ok:** Change the game to: {gameType} ** {gameName} **')

    @config.command()
    @commands.has_role('Bot Manager')
    async def changestatus(self, ctx, status: str):
        '''Changes the online status of the bot (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            nextcordStatus = nextcord.Status.invisible
        elif status == 'idle':
            nextcordStatus = nextcord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            nextcordStatus = nextcord.Status.dnd
        else:
            nextcordStatus = nextcord.Status.online
        await self.bot.change_presence(status=nextcordStatus)
        await ctx.send(f'**:ok:** Change status to: **{nextcordStatus}**')

    @config.command(aliases=['guilds'])
    @commands.has_role('Bot Manager')
    async def servers(self, ctx):
        '''Lists the current connected guilds (BOT OWNER ONLY)'''
        msg = '```py\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @config.command()
    @commands.is_owner()
    async def leaveserver(self, ctx, guildid: int):
        '''Exits a server (BOT OWNER ONLY)
        Example:
        -----------
        :leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Successful exit from {guild.name}!'
            else:
                msg = ":x: Couldn't find a suitable guild for this ID!"
        await ctx.send(msg)

    @config.command(hidden=True)
    @commands.is_owner()
    async def nickname(self, ctx, *name):
        '''Changes the server nickname of the bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f'Changed my server nickname to: **{nickname}**'
        else:
            msg = f'Reset my server nickname on: **{ctx.me.name}**'
        await ctx.send(msg)

    @config.command()
    async def setprefix(self, ctx, prefix = None):
        if prefix is None:
            ctx.send("You need to specify a prefix")
        else:    
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, ctx.guild.id,))
                    await ctx.send(f"updated prefix to '{prefix}'")
                else:
                    await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", ("!", ctx.guild.id,))
                    await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, ctx.guild.id,))
                        await ctx.send(f"updated prefix to '{prefix}'")
                    else:
                        return
            await self.bot.db.commit()

    @config.command()
    @commands.guild_only()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Toggle commands on or off."""
        command = self.bot.get_command(command)
        if command == None:
            await ctx.send("couldn't find that command ._.")
        elif ctx.command == command:
            await ctx.send('you can not disable this command._.')
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f'command {command.qualified_name} has been {ternary}')

    @config.command(name="list")
    @commands.guild_only()
    @commands.is_owner()
    async def list_extensions(self, ctx):
        """List of all cogs."""
        list = nextcord.Embed(title="Cogs List",
                              description="List of all cogs")
        list.add_field(name="startup(Loaded automatically)", value="1. button_roles\n2.error\n3.help\n4.rules\n4.utility\n4.welcome")
        list.add_field(name="extra", value="1.docs\n2.formatting\n3.ping\n4.random")
        list.add_field(name="alt", value="1.channel\n2.leveling\n3.moderation\n4.starboard")
        list.add_field(name="testing", value="1.blacklist\n2.embed\n3.music\n4.testing")
        await ctx.send(embed=list)

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def load(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()


    @load.command(name="startup")
    @commands.is_owner()
    async def load_startup(self, ctx, *, extension):
        """Load startup cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.load_extension(f"startup.{extension}")
            await ctx.send(f"{extension} loaded")
            print(f"{extension} loaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @load.command(name="extra")
    @commands.is_owner()
    async def load_extra(self, ctx, *, extension):
        """Load extra cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.load_extension(f"extra.{extension}")
            await ctx.send(f"{extension} loaded")
            print(f"{extension} loaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @load.command(name="alt")
    @commands.is_owner()
    async def load_alt(self, ctx, *, extension):
        """Load alt cogs.(use list command to see available cogs)"""
        if ctx.author.id == 741118153299591240:
            self.bot.load_extension(f"alt.{extension}")
            await ctx.send(f"{extension} loaded")
            print(f"{extension} loaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @load.command(name="test")
    @commands.is_owner()
    async def load_test(self, ctx, *, extension):
        """Load alt cogs.(use list command to see available cogs)"""
        if ctx.author.id == 741118153299591240:
            self.bot.load_extension(f"testing.{extension}")
            await ctx.send(f"{extension} loaded")
            print(f"{extension} loaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def loadall(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()


    @loadall.command(name="startup")
    @commands.is_owner()
    async def loadall_startup(self, ctx):
        """Load all startup cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("startup"):
                self.bot.load_extension(f"startup.{folder}")
                await ctx.send(f"Loaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @loadall.command(name="extra")
    @commands.guild_only()
    @commands.is_owner()
    async def loadall_extra(self, ctx):
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("extra"):
                self.bot.load_extension(f"extra.{folder}")
                await ctx.send(f"Loaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @loadall.command(name="alt")
    @commands.guild_only()
    @commands.is_owner()
    async def loadall_alt(self, ctx):
        """Load all alt cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("alt"):
                self.bot.load_extension(f"alt.{folder}")
                await ctx.send(f"Loaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @loadall.command(name="test")
    @commands.guild_only()
    @commands.is_owner()
    async def loadall_test(self, ctx):
        """Load all alt cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("testing"):
                self.bot.load_extension(f"testing.{folder}")
                await ctx.send(f"Loaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def reload(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()

    @reload.command(name="startup")
    @commands.is_owner()
    async def reload_startup(self, ctx, *, extension):
        """Reload startup cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.reload_extension(f"startup.{extension}")
            await ctx.send(f"{extension} reloaded")
            print(f"{extension} reloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @reload.command(name="extra")
    @commands.is_owner()
    async def reload_extra(self, ctx, *, extension):
        """Reload extra cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.reload_extension(f"extra.{extension}")
            await ctx.send(f"{extension} reloaded")
            print(f"{extension} reloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @reload.command(name="alt")
    @commands.is_owner()
    async def reload_alt(self, ctx, *, extension):
        """Reload alt cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.reload_extension(f"alt.{extension}")
            await ctx.send(f"{extension} reloaded")
            print(f"{extension} reloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @reload.command(name="test")
    @commands.is_owner()
    async def reload_test(self, ctx, *, extension):
        """Reload alt cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.reload_extension(f"testing.{extension}")
            await ctx.send(f"{extension} reloaded")
            print(f"{extension} reloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unload(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()
        
    @unload.command(name="startup")
    @commands.is_owner()
    async def unload_startup(self, ctx, *, extension):
        """Unload startup cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.unload_extension(f"startup.{extension}")
            await ctx.send(f"{extension} unloaded")
            print(f"{extension} unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @unload.command(name="extra")
    @commands.is_owner()
    async def unload_extra(self, ctx, *, extension):
        """Unload extra cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.unload_extension(f"extra.{extension}")
            await ctx.send(f"{extension} unloaded")
            print(f"{extension} unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @unload.command(name="alt")
    @commands.is_owner()
    async def unload_alt(self, ctx, *, extension):
        """Unload alt cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.unload_extension(f"alt.{extension}")
            await ctx.send(f"{extension} unloaded")
            print(f"{extension} unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @unload.command(name="test")
    @commands.is_owner()
    async def unload_test(self, ctx, *, extension):
        """Unload alt cogs."""
        if ctx.author.id == 741118153299591240:
            self.bot.unload_extension(f"testing.{extension}")
            await ctx.send(f"{extension} unloaded")
            print(f"{extension} unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unloadall(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()

    @unloadall.command(name="extra")
    @commands.guild_only()
    @commands.is_owner()
    async def unloadall_extra(self, ctx):
        """Unload all extra cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("extra"):
                self.bot.unload_extension(f"extra.{folder}")
                await ctx.send(f"unloaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @unloadall.command(name="alt")
    @commands.guild_only()
    @commands.is_owner()
    async def unloadall_alt(self, ctx):
        """Unload all alt cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("alt"):
                self.bot.unload_extension(f"alt.{folder}")
                await ctx.send(f"unloaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @unloadall.command(name="test")
    @commands.guild_only()
    @commands.is_owner()
    async def unloadall_test(self, ctx):
        """Unload all alt cogs."""
        if ctx.author.id == 741118153299591240:
            for folder in os.listdir("testing"):
                self.bot.unload_extension(f"testing.{folder}")
                await ctx.send(f"unloaded {folder}.")
        else:
            await ctx.send("Only bot devs can run this command")

    @config.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def check(self, ctx):
        """test"""
        await ctx.channel.trigger_typing()

    @check.command(name="startup")
    @commands.is_owner()
    async def check_startup(self, ctx, *, extension):
        """Check startup cogs."""
        if ctx.author.id == 741118153299591240:
            try:
                self.bot.load_extension(f"startup.{extension}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{extension} is loaded")
                print(f"{extension} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{extension} not found")
                print(f"{extension} not found")
            else:
                await ctx.send("{extension} is unloaded")
                self.bot.unload_extension(f"startup.{extension}")
                print(f"{extension} is unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @check.command(name="extra")
    @commands.is_owner()
    async def check_extra(self, ctx, *, extension):
        """ Check extra cogs."""
        if ctx.author.id == 741118153299591240:
            try:
                self.bot.load_extension(f"extra.{extension}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{extension} is loaded")
                print(f"{extension} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{extension} not found")
                print(f"{extension} not found")
            else:
                await ctx.send("{extension} is unloaded")
                self.bot.unload_extension(f"extra.{extension}")
                print(f"{extension} is unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @check.command(name="alt")
    @commands.is_owner()
    async def check_alt(self, ctx, *, extension):
        """Check alt cogs."""
        if ctx.author.id == 741118153299591240:
            try:
                self.bot.load_extension(f"alt.{extension}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{extension} is loaded")
                print(f"{extension} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{extension} not found")
                print(f"{extension} not found")
            else:
                await ctx.send("{extension} is unloaded")
                self.bot.unload_extension(f"alt.{extension}")
                print(f"{extension} is unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

    @check.command(name="test")
    @commands.is_owner()
    async def check_test(self, ctx, *, extension):
        """Check alt cogs."""
        if ctx.author.id == 741118153299591240:
            try:
                self.bot.load_extension(f"testing.{extension}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{extension} is loaded")
                print(f"{extension} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{extension} not found")
                print(f"{extension} not found")
            else:
                await ctx.send("{extension} is unloaded")
                self.bot.unload_extension(f"alt.{extension}")
                print(f"{extension} is unloaded")
        else:
            await ctx.send("Only bot devs can run this command")

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))