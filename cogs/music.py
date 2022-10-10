import discord
from discord.ext import commands
import youtube_dl
import asyncio

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 
    async def async_init(self):
        self.queue = []
        self.current = None
        self.play_next_song = asyncio.Event()
        self.bot.loop.create_task(self.song_player())
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Dude, I'm not even in a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            channel = ctx.message.author.voice.channel
            await voice_channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        else:
            await ctx.voice_client.move_to(voice_channel)
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self,ctx, url):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        else:
            await ctx.send("You are not in a voice channel, please join one and try again.")
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)
    @commands.command()
    async def pause(self, ctx : commands.Context):
        await ctx.send("Paused")
        await ctx.voice_client.pause()
        
    @commands.command()
    async def resume(self, ctx : commands.Context):
        await ctx.send("Resumed")
        await ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx : commands.Context):
        await ctx.send("Stopped")
        await ctx.voice_client.stop()
async def setup(bot):
    await bot.add_cog(Music(bot))