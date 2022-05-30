####################### DEPRECATED #########################
# Imports
import glob
import os
import discord
import youtube_dl
from time import sleep
from discord.ext import commands

# Class to hold functions for general commands
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Leave voice channel
    @commands.command()
    async def leave(self, ctx):
        if await self.channel_check(ctx) is True:
            channel = ctx.author.guild.voice_client
            await channel.disconnect(force=True)

        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Join the voice channel you are in
    @commands.command()
    async def join(self, ctx):
        if await self.channel_check(ctx) is True:
            channel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)
            await channel.connect()
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Play a YouTube url song
    @commands.command()
    async def play(self, ctx, url: str):
        if await self.channel_check(ctx) is True:
            # Iterate over the list of filepaths & remove each file.
            fileList = glob.glob("*.webm", recursive=True)
            for filePath in fileList:
                try:
                    os.remove(filePath)
                except OSError:
                    print("Error while deleting file")
            song_there = os.path.isfile("song.webm")
            try:
                if song_there:
                    os.remove("song.webm")
            except PermissionError:
                await ctx.send(
                    "Wait for the current playing audio to end or use the 'stop' command"
                )
                return

            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                "format": "249/250/251",
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".webm"):
                    os.rename(file, "song.webm")
            voice.play(discord.FFmpegOpusAudio("song.webm"))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Pause current song
    @commands.command()
    async def pause(self, ctx):
        if await self.channel_check(ctx) is True:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.pause()
            else:
                await ctx.send("Currently no audio is playing.")
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Resume current song
    @commands.command()
    async def resume(self, ctx):
        if await self.channel_check(ctx) is True:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_paused():
                voice.resume()
            else:
                await ctx.send("The audio is not paused.")
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Stop current song
    @commands.command()
    async def stop(self, ctx):
        if await self.channel_check(ctx) is True:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.stop()
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Make sure commands are in the bot channel
    async def channel_check(self, ctx):
        if (
            ctx.message.channel.name == "berd-bot🔌"
            or ctx.message.channel.name == "bot-test-🔌"
        ):
            return True
        else:
            return False


# Setup function for cog
def setup(client):
    client.add_cog(Music(client))
