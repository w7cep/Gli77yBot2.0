from nextcord.ext import commands
import nextcord
import os

class Testing (commands.Cog, name="Testing"):
    """Testing commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    async def adduser(self, ctx, member: nextcord.Member= None):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE guild = ?", (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE users SET id = ? WHERE guild = ?", (member.id, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO users (id, guild) Values (?, ?)", (member.id, ctx.guild.id,))
        await self.bot.db.commit()            
    
    @commands.command(hidden=True)
    async def removeuser(self, ctx, member: nextcord.Member = None):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE guild = ?", (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM users WHERE id = ? AND guild = ?", (member.id, ctx.guild.id,))
        await self.bot.db.commit()

    @commands.command()
    @commands.is_owner()
    async def discriminator(self, ctx, disc: str):
        '''Returns users with the respective discriminator'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(":x: Couldn't find anyone")

def setup(bot: commands.Bot):
    bot.add_cog(Testing(bot))