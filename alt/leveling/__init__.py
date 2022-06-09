import nextcord
from nextcord.ext import commands
import aiosqlite
import asyncio
import random
from easy_pil import *

class LevelingCog(commands.Cog, name="Leveling"):
    """Welcome users when they join"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
       
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return
                           
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            level = await cursor.fetchone()
            
            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))
                await self.bot.db.commit()
                
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0
                
            if level < 5:
                xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
            else:
                rand = random.randint(1, (level//4))
                if rand == 1:
                    xp += random.randint(1, 3)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,)) 
            if xp >= 100:
                level += 1
                await cursor.execute("SELECT role FROM levelSettings WHERE levelreq = ? AND guild = ?", (level, guild.id,))
                role = await cursor.fetchone()
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
                if role:
                    role = role[0]
                    role = guild.get_role(role)
                    try:
                        await author.add_roles(role)
                        await message.channel.send(f"{author.mention} has just leveled up to **{level}** and received the **{role.name}** role.")
                    except nextcord.HTTPException:  
                        await message.channel.send(f"{author.mention} has leveled up to level **{level}**! [WAS NOT ABLE TO GIVE LEVEL ROLE]")
                await message.channel.send(f"{author.mention} has leveled up to level **{level}**!")        
        await self.bot.db.commit()
        """await self.bot.process_commands(message)"""
        
    @commands.command()
    async def level(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        async with self.bot.db.cursor() as cursor:  
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return  
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            level = await cursor.fetchone()
            
            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
                await self.bot.db.commit()
                
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            user_data = {
                "name": f"{member.name}#{member.discriminator}",
                "xp": xp,
                "level": level,
                "next_level_up": 100,
                "percentage": xp,
            }
            
            background = Editor(Canvas((900, 300),color="#141414"))
            profile_picture = await load_image_async(str(member.avatar.url))
            profile = Editor(profile_picture).resize((150, 150)).circle_image()
            
            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)
            
            card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
            
            background.polygon(card_right_shape, color="#FFFFFF")
            background.paste(profile, (30, 30))
            
            background.rectangle((30, 220), width=650, height=40, color="#FFFFFF")
            background.bar((30, 220), max_width=650, height=40, percentage=user_data["percentage"], color="#282828", radius=20,)
            background.text((200, 40), user_data["name"], font=poppins, color="#FFFFFF")
            
            background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
            background.text(
                (200, 130),
                f"Level - {user_data['level']} | XP = {user_data['xp']}/{user_data['next_level_up']}",
                font = poppins_small,
                color = "#FFFFFF",
            )
            
            file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
            await ctx.send(file=file)
            
    @commands.command()
    async def rewards(self, ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0] == 1:
                    return await ctx.send("the leveling system is disabled in this server!")        
            await cursor.execute("SELECT * FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            rolelevels = await cursor.fetchall()
            if not rolelevels:
                return await ctx.send("No role levels have been setup for this guild!")
            em = nextcord.Embed(title="role levels", description="role levels for this server")
            for role in rolelevels:
                em.add_field(name=f"level {role[2]}", value=f"{ctx.guild.get_role(role[1])}", inline=False)
            await ctx.send(embed=em)
    
    @commands.command()
    async def leaderboard(self, ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0] == 1:
                    return await ctx.send("the leveling system is disabled in this server!")
            await cursor.execute("SELECT level, xp, user From levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10", (ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                em = nextcord.Embed(title="Leveling Leaderboard")
                count = 0
                for table in data:
                    count += 1
                    user = ctx.guild.get_member(table[2])
                    em.add_field(name=f"{count}. {user.name}", value=f"Level:**{table[0]}** | XP:**{table[1]}**", inline=False)
                return await ctx.send(embed=em)
            return await ctx.send("there are no users stored in the leaderboard")
        
    @commands.group()
    async def slvl(self, ctx):
        return
    
    @slvl.command()
    @commands.has_permissions(manage_guild=True)
    async def setrole(self, ctx, level:int, *, role: nextcord.Role):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0] == 1:
                    return await ctx.send("the leveling system is disabled in this server!")  
            await cursor.execute("SELECT role FROM levelSettings WHERE role = ? AND guild = ?", (role.id, ctx.guild.id,))
            roleTF = await cursor.fetchone()
            await cursor.execute("SELECT role FROM levelSettings WHERE levelreq = ? AND guild = ?", (level, ctx.guild.id,))
            levelTF = await cursor.fetchone()   
            if roleTF or levelTF:
                return await ctx.send(" a role or level setting for that value already exists")
            await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)", (True, role.id, level, ctx.guild.id,))
            await self.bot.db.commit()
        await ctx.send("updated that level role!")  
              
    @slvl.command()
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if levelsys[0]:
                    return await ctx.send("the leveling system is already enabled")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?", (True, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)", (True, 0, 0, ctx.guild.id,))
            await ctx.send("enabled the leveling system!")
        await self.bot.db.commit()

    @slvl.command()
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0]:
                    return await ctx.send("the leveling system is already disabled")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?", (False, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)", (False, 0, 0, ctx.guild.id,))
            await ctx.send("disabled the leveling system!")
        await self.bot.db.commit()
        
    # setup functions for bot
def setup(bot):
    bot.add_cog(LevelingCog(bot))