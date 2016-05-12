import asyncio
import discord
import pafy
from Commands.Dependencies import youtube as yt
from discord.ext import commands as client

try:
    print("Loading opus")
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus-0.dll')
except:
    opus = None
else:
    opus = True
    print('opus Status= {}'.format(discord.opus.is_loaded()))


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.play_next = asyncio.Event()
        self.player = None
        self.current = None

    def play_next_song(self):
        self.bot.loop.call_soon_threadsafe(self.play_next.set)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def join_voice(self, ctx):
        if not ctx.message.author.voice_channel == None:
            active_channel = ctx.message.author.voice_channel
            if active_channel == ctx.message.server.me.voice_channel:
                return True
            elif not ctx.message.server.me.voice_channel == None and len(ctx.message.server.me.voice_channel.voice_members) > 1:
                return True
            else:
                try:
                    await self.bot.join_voice_channel(ctx.message.author.voice_channel)
                    return True
                except Exception as e:
                    print(e)
                    await self.bot.say('Couldnt join the voice channel')
                    return False
        else:
            await self.bot.say('You have to be in a voice channel first')
            return False

    async def play_song(self, ctx, url):
        if self.player is not None and self.player.is_playing():
            #self.queue.put(VoiceEntry(ctx,url))
            #self.play_next_song()
            return
        print(self.bot.voice_client_in(ctx.message.server))
        while True:
            if not self.bot.is_voice_connected(ctx.message.server):
                await self.join_voice(ctx)
            #print(self.bot.voice_client_in(ctx.message.server))
            await self.queue.put(VoiceEntry(ctx,url))
            self.play_next.clear()
            self.current = await self.queue.get()
           # print(self.current.song)
            try:
                self.player = self.bot.voice_client_in(ctx.message.server).create_ffmpeg_player(self.current.song, after=self.play_next_song)
            except:
                self.player = self.bot.voice_client_in(ctx.message.server).create_ffmpeg_player(self.current.song)
            self.player.start()
            await self.play_next.wait()

    @client.command(pass_context = True)
    async def play(self, ctx, url):
        await self.play_song(ctx, url)

    @client.command()
    async def test_url(self, url):
        await self.bot.say(yt.download_url(url))

class VoiceEntry:
    def __init__(self, ctx, url):
        self.requester = ctx.message.author
        self.channel = ctx.message.channel
        self.song = None
        if yt.is_valid_url(yt.search(url)[0]):
            video = pafy.new(yt.search(url)[0])
            best_audio = video.getbestaudio()
            self.song = best_audio.url


    
def setup(bot):
    bot.add_cog(Music(bot))