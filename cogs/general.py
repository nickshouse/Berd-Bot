# Imports
import discord
import random
from time import sleep
from discord.ext import commands


# Class to hold functions for general commands
class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Tell when bot is online
    @commands.Cog.listener()
    async def on_ready(self):
        print("Berd Bot is online")

    @commands.command()
    async def test(self, ctx):
        fish_chance = random.randint(1, 20)
        await ctx.send(fish_chance)

    # Show list of commands
    @commands.command()
    async def help(self, ctx):
        if await self.channel_check(ctx) is True:
            cmds = [
                "```!help - Shows list of commands",
                "\n!join - Makes the bot join the voice channel you are in",
                "\n!leave - Makes the bot leave the voice channel it's in",
                "\n!pause - (deprecated)"
                "\n!resume - (deprecated)"
                "\n!stop - (deprecated)"
                "\n!play - (deprecated)",
                "\n!8ball - Attempts to answer your question"
                "\nExample usage: !8ball should I eat the burger"
                "\nNote: Still in development",
                "\n!d - Dice roller, must specify dice sides and dice amount"
                "\nExample usage: !d 20 3"
                "\nNote: May take more time to roll with many dice",
                "\n!roulette - You have a 1 in 6 chance to get shot"
                "\nNote: Getting shot results in an immediate kick from the server"
                "\n      Users with high privledges cannot be kicked"
                "\n      Users that are kicked will be reinvited back to the server",
                "\n!fishing - Shows list of fishing commands",
                "\n!eco - WIP```",
            ]
            await ctx.send("\n".join(cmds))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Meme commands
    @commands.command()
    async def aleppo(self, ctx):
        if await self.channel_check(ctx) is True:
            await ctx.send("Who?")
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    @commands.command()
    async def flake(self, ctx):
        if await self.channel_check(ctx) is True:
            responses = ["Why didn’t you buy me Matt"]
            await ctx.send(random.choice(responses))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Magic 8 Ball
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        if await self.channel_check(ctx) is True:
            responses = [
                "You may rely on it.",
                "Perhaps...",
                "Sure",
                "Doesn't look good.",
                "It is absolute.",
                "I'm getting hungry.",
                "Yeah",
                "Nah",
                "Maybe",
            ]
            firstword = (
                "want wanna who what whats what's wat wats when where why would "
                "wouldnt wouldn't will wont won't were werent weren't whom "
                "was wasnt wasn't which has hasnt hasn't have havent haven't "
                "how had hadnt hadn't should shouldnt shouldn't shall can cant "
                "can't could couldnt couldn't do dont don't does is isnt isn't are arent aren't am ".split()
            )
            # Answers
            if question.lower().startswith(
                "will andy pick me"
            ) or question.lower().startswith("will andy pick me?"):
                await ctx.send("Don't count on it.")
            else:
                if any(question.lower().startswith(w) for w in firstword):
                    await ctx.send(random.choice(responses))
                else:
                    await ctx.send("I'm not sure.")
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Dice roller
    @commands.command()
    async def d(self, ctx, num: int, amount: int):
        if await self.channel_check(ctx) is True:
            for i in range(amount):
                await ctx.send(random.randint(1, num))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Roulette
    @commands.command()
    async def roulette(self, ctx):
        if await self.channel_check(ctx) is True:
            user = ctx.author
            responses = ["click", "click", "click", "click", "click", "BANG"]
            if random.choice(responses) == "BANG":
                await ctx.send(file=discord.File("./png/BANG.png"))
                async for member in ctx.guild.fetch_members(limit=None):
                    if ctx.author.id == member.id:
                        link = await ctx.channel.create_invite()
                        await user.send(
                            "The shadow of Death has fallen upon you...\nYou were shot in an unlucky game of roulette.\n\n**Click this link to be revived:**\n"
                            + str(link)
                        )
                        await member.kick()
            else:
                await ctx.send(file=discord.File("./png/click.png"))
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
    client.add_cog(General(client))
