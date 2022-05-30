# Imports
import os
import discord
import bot_token
from time import sleep
from discord.ext import commands


# All commands must start with !
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
client.remove_command("help")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# Shut down the bot, must wait for host to turn it back on.
@client.command()
@commands.has_permissions(administrator=True)
async def close(ctx):
    await client.close()


client.run(bot_token.your_bot_token)
