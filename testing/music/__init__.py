from nextcord.ext import commands
import nextcord
import wavelink
import datetime
class Music(commands.Cog, name="Music"):
    """Music commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalinkinc.ml", port=443, password="incognito", https=True)
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready!!")
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client
        
        if vc.loop:
            return await vc.play(track)
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Now playing: {next_song.title}")
    
    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await ctx.send(f"Now playing: {search.title}")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added `{search.title}` to the queue!")
        vc.ctx = ctx
        setattr(vc, "loop", False)
        
    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.pause()
        await ctx.send("Music has been paused!")
        
    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("I'm already playing music")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.resume()
        await ctx.send("Music has been resumed!")
    
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.stop()
        await ctx.send("Music has been stopped!")    

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.disconnect()
        await ctx.send("Gli77yBot has been disconnected!") 

    @commands.command()
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)
        if vc.loop:
            return await ctx.send("Loop is now Enabled!")
        else:
            return await ctx.send("Loop is now Disabled!")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.queue.is_empty:
            return await ctx.send("Queue is empty")
        em = nextcord.Embed(title="Queue")
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f"Song num {song_count}", value=f"`{song.title}`")
        return await ctx.send(embed=em)
    
    @commands.command()
    async def volume(self,ctx: commands.Context, volume: int):
        if not ctx.voice_client:
            return await ctx.send("I'm already playing music")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if volume > 100:
            return await ctx.send("Volume can't go that high!")
        elif volume <0:
            return await ctx.send("Volume can't go that low!")
        await ctx.send(f"Set the volume to `{volume}%`")
        return await vc.set_volume(volume)
    
    @commands.command()
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("I'm already playing music")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("You need to join a voice channel first!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("Nothing is playing!")
        em = nextcord.Embed(title=f"Now playing {vc.track.title}", description=f"Artist: {vc.track.author}")
        em.add_field(name="Duration", value=f"`{str(datetime.timedelta(seconds=vc.track.duration))}`")
        em.add_field(name="Extra info", value=f"Song URL: [Click ME]({str(vc.track.uri)})")
        return await ctx.send(embed=em)
        
def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))