# Imports
import discord
import random
import json
import asyncio
from time import sleep
from discord.ext import commands


# Class to hold functions for Fishing commands
class Fishing(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Help list
    @commands.command()
    async def fishing(self, ctx):
        if await self.channel_check(ctx) is True:
            await self.create_fisher(ctx.author)
            cmds = [
                "```!cast - Cast your line out to the ocean",
                "\n!total - Shows the total amount of fish you've caught",
                "\n!pb - Shows the best fish you've caught",
                "\n!best - Shows the best fish in the server",
                "\n!last - Shows the last fish you've caught",
                "\n!classes - Shows list of possible class rankings for fish```",
            ]
            await ctx.send("\n".join(cmds))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Cast
    @commands.command()
    @commands.cooldown(20, 3600, commands.BucketType.user)
    async def cast(self, ctx):
        if await self.channel_check(ctx) is True:
            await self.create_fisher(ctx.author)
            users = await self.get_fishing_data()

            await ctx.send("You cast your line out into the ocean...")
            async with ctx.typing():
                await asyncio.sleep(5)

            fish_chance = random.randint(1, 20)
            if fish_chance == 1:  # JUNK
                await self.cast_junk(ctx, users)
            elif fish_chance >= 2 and fish_chance < 10:  # SMALL FISH
                await self.cast_small(ctx, users)
            elif fish_chance >= 10 and fish_chance < 15:  # MEDIUM FISH
                await self.cast_medium(ctx, users)
            elif fish_chance >= 15 and fish_chance < 18:  # LARGE FISH
                await self.cast_large(ctx, users)
            elif fish_chance >= 18:  # GRAND FISH
                if users[str(ctx.author.id)]["total_fish"] >= 100:
                    await self.cast_grand(ctx, users)
                else:
                    await self.cast_break(ctx)
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Cooldown
    @cast.error
    async def cast_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after) % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            await ctx.send(
                f"That's enough fishing for now.\nTry again in {minutes} minutes and {seconds} seconds..."
            )

    # Junk catches
    async def cast_junk(self, ctx, users):
        junk_names = [
            "Broken Pot",
            "Old Shoe",
            "Fishing Rod",
            "Tin Can",
            "Plastic Bottle",
            "Plastic Bag",
            "Rusty Pipe",
            "Crusty Jeans",
            "Broken Lock",
            "Novelty Fish",
            "Toy Car",
            "Cardboard Box",
            "copy of E.T. the Extra-Terrestrial",
            "Rubber Tire",
        ]
        junk_class = 7
        junk_current = random.choice(junk_names)
        with open("./json/fishing.json", "w") as f:
            json.dump(users, f, indent=4)
        await ctx.send(f"**You caught a** ***{junk_current}!...***\nClass: Junk")

    # Small fish
    async def cast_small(self, ctx, users):
        if random.randint(1, 3) > 1:
            small_fish_names = [
                "Anchovy",
                "Crab",
                "Lobster",
                "Snail",
                "Smallmouth Bass",
                "Steelhead Trout",
                "Yellow Perch",
                "Goldfish",
                "Chub",
                "Sea Horse",
                "Bluegill",
                "Black Crappie",
                "Clownfish",
                "Oscar",
                "Yellow Croaker",
                "Lionfish",
            ]
            small_fish_weight_pounds = random.randint(1, 5)
            small_fish_weight_ounces = random.randint(0, 15)
            small_fish_length_feet = random.randint(0, 1)
            small_fish_length_inches = random.randint(1, 11)
            small_fish_class = 6
            small_fish_current = random.choice(small_fish_names)
            await self.assign_last(
                ctx,
                users,
                small_fish_weight_pounds,
                small_fish_weight_ounces,
                small_fish_length_feet,
                small_fish_length_inches,
                small_fish_class,
                small_fish_current,
            )
            users[str(ctx.author.id)]["total_fish"] += 1
            if (
                users[str(ctx.author.id)]["last_fish_class"]
                < users[str(ctx.author.id)]["best_fish_class"]
            ):
                await self.assign_best(
                    ctx,
                    users,
                    small_fish_weight_pounds,
                    small_fish_weight_ounces,
                    small_fish_length_feet,
                    small_fish_length_inches,
                    small_fish_class,
                    small_fish_current,
                )
            elif (
                users[str(ctx.author.id)]["last_fish_class"]
                == users[str(ctx.author.id)]["best_fish_class"]
            ):
                if (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    > users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    await self.assign_best(
                        ctx,
                        users,
                        small_fish_weight_pounds,
                        small_fish_weight_ounces,
                        small_fish_length_feet,
                        small_fish_length_inches,
                        small_fish_class,
                        small_fish_current,
                    )
                elif (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    == users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    if (
                        users[str(ctx.author.id)]["last_fish_ounces"]
                        > users[str(ctx.author.id)]["best_fish_ounces"]
                    ):
                        await self.assign_best(
                            ctx,
                            users,
                            small_fish_weight_pounds,
                            small_fish_weight_ounces,
                            small_fish_length_feet,
                            small_fish_length_inches,
                            small_fish_class,
                            small_fish_current,
                        )

            with open("./json/fishing.json", "w") as f:
                json.dump(users, f, indent=4)
            await ctx.send(
                f"**You caught a** ***{small_fish_current}!***\nSize: {small_fish_length_feet} feet and {small_fish_length_inches} inches\nWeight: {small_fish_weight_pounds} pounds and {small_fish_weight_ounces} ounces\nClass: Small"
            )
        else:
            await self.cast_fail(ctx)

    # Medium fish
    async def cast_medium(self, ctx, users):
        if random.randint(1, 3) > 1:
            medium_fish_names = [
                "Blobfish",
                "Paddlefish",
                "Sea Bass",
                "Walleye",
                "Muskellunge",
                "Catfish",
                "Snapper",
                "Pink Salmon",
                "Albino Carp",
                "Cutthroat Trout",
                "Tautog",
                "Blackfish",
                "Dogfish",
                "Rockfish",
                "Needlefish",
                "Northern Pike",
                "Anglerfish",
                "Electric Eel",
                "Albacore",
                "Turbot",
                "Burbot",
                "Lumpfish",
                "Haddock",
                "Chum Salmon",
            ]
            medium_fish_weight_pounds = random.randint(6, 50)
            medium_fish_weight_ounces = random.randint(0, 15)
            medium_fish_length_feet = random.randint(2, 4)
            medium_fish_length_inches = random.randint(1, 11)
            medium_fish_class = 5
            medium_fish_current = random.choice(medium_fish_names)
            await self.assign_last(
                ctx,
                users,
                medium_fish_weight_pounds,
                medium_fish_weight_ounces,
                medium_fish_length_feet,
                medium_fish_length_inches,
                medium_fish_class,
                medium_fish_current,
            )
            users[str(ctx.author.id)]["total_fish"] += 1
            if (
                users[str(ctx.author.id)]["last_fish_class"]
                < users[str(ctx.author.id)]["best_fish_class"]
            ):
                await self.assign_best(
                    ctx,
                    users,
                    medium_fish_weight_pounds,
                    medium_fish_weight_ounces,
                    medium_fish_length_feet,
                    medium_fish_length_inches,
                    medium_fish_class,
                    medium_fish_current,
                )
            elif (
                users[str(ctx.author.id)]["last_fish_class"]
                == users[str(ctx.author.id)]["best_fish_class"]
            ):
                if (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    > users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    await self.assign_best(
                        ctx,
                        users,
                        medium_fish_weight_pounds,
                        medium_fish_weight_ounces,
                        medium_fish_length_feet,
                        medium_fish_length_inches,
                        medium_fish_class,
                        medium_fish_current,
                    )
                elif (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    == users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    if (
                        users[str(ctx.author.id)]["last_fish_ounces"]
                        > users[str(ctx.author.id)]["best_fish_ounces"]
                    ):
                        await self.assign_best(
                            ctx,
                            users,
                            medium_fish_weight_pounds,
                            medium_fish_weight_ounces,
                            medium_fish_length_feet,
                            medium_fish_length_inches,
                            medium_fish_class,
                            medium_fish_current,
                        )

            with open("./json/fishing.json", "w") as f:
                json.dump(users, f, indent=4)
            await ctx.send(
                f"**You caught a** ***{medium_fish_current}!***\nSize: {medium_fish_length_feet} feet and {medium_fish_length_inches} inches\nWeight: {medium_fish_weight_pounds} pounds and {medium_fish_weight_ounces} ounces\nClass: Medium"
            )
        else:
            await self.cast_fail(ctx)

    # Large fish
    async def cast_large(self, ctx, users):
        if random.randint(1, 3) > 1:
            large_fish_names = [
                "King Salmon",
                "Cod",
                "Dolphin",
                "Sturgeon",
                "Sea Turtle",
                "Bull Shark",
                "Great Barracuda",
                "Leerfish",
                "Red Drum",
                "Dogtooth Tuna",
                "Cobia",
                "Mackerel",
                "Monkfish",
                "Toothfish",
                "Sablefish",
            ]
            large_fish_weight_pounds = random.randint(50, 250)
            large_fish_weight_ounces = random.randint(0, 15)
            large_fish_length_feet = random.randint(3, 8)
            large_fish_length_inches = random.randint(1, 11)
            large_fish_class = 4
            large_fish_current = random.choice(large_fish_names)
            await self.assign_last(
                ctx,
                users,
                large_fish_weight_pounds,
                large_fish_weight_ounces,
                large_fish_length_feet,
                large_fish_length_inches,
                large_fish_class,
                large_fish_current,
            )
            users[str(ctx.author.id)]["total_fish"] += 1
            if (
                users[str(ctx.author.id)]["last_fish_class"]
                < users[str(ctx.author.id)]["best_fish_class"]
            ):
                await self.assign_best(
                    ctx,
                    users,
                    large_fish_weight_pounds,
                    large_fish_weight_ounces,
                    large_fish_length_feet,
                    large_fish_length_inches,
                    large_fish_class,
                    large_fish_current,
                )
            elif (
                users[str(ctx.author.id)]["last_fish_class"]
                == users[str(ctx.author.id)]["best_fish_class"]
            ):
                if (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    > users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    await self.assign_best(
                        ctx,
                        users,
                        large_fish_weight_pounds,
                        large_fish_weight_ounces,
                        large_fish_length_feet,
                        large_fish_length_inches,
                        large_fish_class,
                        large_fish_current,
                    )
                elif (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    == users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    if (
                        users[str(ctx.author.id)]["last_fish_ounces"]
                        > users[str(ctx.author.id)]["best_fish_ounces"]
                    ):
                        await self.assign_best(
                            ctx,
                            users,
                            large_fish_weight_pounds,
                            large_fish_weight_ounces,
                            large_fish_length_feet,
                            large_fish_length_inches,
                            large_fish_class,
                            large_fish_current,
                        )

            with open("./json/fishing.json", "w") as f:
                json.dump(users, f, indent=4)
            await ctx.send(
                f"**You caught a** ***{large_fish_current}!***\nSize: {large_fish_length_feet} feet and {large_fish_length_inches} inches\nWeight: {large_fish_weight_pounds} pounds and {large_fish_weight_ounces} ounces\nClass: Large"
            )
        else:
            await self.cast_fail(ctx)

    # Grand fish
    async def cast_grand(self, ctx, users):
        if random.randint(1, 3) > 1:
            grand_fish_names = [
                "Goliath Grouper",
                "Black Marlin",
                "Bluefin Tuna",
                "Sawfish",
                "Halibut",
            ]
            grand_fish_weight_pounds = random.randint(500, 2000)
            grand_fish_weight_ounces = random.randint(0, 15)
            grand_fish_length_feet = random.randint(8, 18)
            grand_fish_length_inches = random.randint(1, 11)
            grand_fish_class = 3
            grand_fish_current = random.choice(grand_fish_names)
            await self.assign_last(
                ctx,
                users,
                grand_fish_weight_pounds,
                grand_fish_weight_ounces,
                grand_fish_length_feet,
                grand_fish_length_inches,
                grand_fish_class,
                grand_fish_current,
            )
            users[str(ctx.author.id)]["total_fish"] += 1
            if (
                users[str(ctx.author.id)]["last_fish_class"]
                < users[str(ctx.author.id)]["best_fish_class"]
            ):
                await self.assign_best(
                    ctx,
                    users,
                    grand_fish_weight_pounds,
                    grand_fish_weight_ounces,
                    grand_fish_length_feet,
                    grand_fish_length_inches,
                    grand_fish_class,
                    grand_fish_current,
                )
            elif (
                users[str(ctx.author.id)]["last_fish_class"]
                == users[str(ctx.author.id)]["best_fish_class"]
            ):
                if (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    > users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    await self.assign_best(
                        ctx,
                        users,
                        grand_fish_weight_pounds,
                        grand_fish_weight_ounces,
                        grand_fish_length_feet,
                        grand_fish_length_inches,
                        grand_fish_class,
                        grand_fish_current,
                    )
                elif (
                    users[str(ctx.author.id)]["last_fish_pounds"]
                    == users[str(ctx.author.id)]["best_fish_pounds"]
                ):
                    if (
                        users[str(ctx.author.id)]["last_fish_ounces"]
                        > users[str(ctx.author.id)]["best_fish_ounces"]
                    ):
                        await self.assign_best(
                            ctx,
                            users,
                            grand_fish_weight_pounds,
                            grand_fish_weight_ounces,
                            grand_fish_length_feet,
                            grand_fish_length_inches,
                            grand_fish_class,
                            grand_fish_current,
                        )

            with open("./json/fishing.json", "w") as f:
                json.dump(users, f, indent=4)
            await ctx.send(
                f"**You caught a** ***{grand_fish_current}!***\nSize: {grand_fish_length_feet} feet and {grand_fish_length_inches} inches\nWeight: {grand_fish_weight_pounds} pounds and {grand_fish_weight_ounces} ounces\nClass: Grand"
            )
        else:
            random.choice(await self.cast_fail(ctx))

    # Assign last fish
    async def assign_last(
        self,
        ctx,
        users,
        fish_weight_pounds,
        fish_weight_ounces,
        fish_length_feet,
        fish_length_inches,
        fish_class,
        fish_current,
    ):
        users[str(ctx.author.id)]["last_fish_name"] = fish_current
        users[str(ctx.author.id)]["last_fish_pounds"] = fish_weight_pounds
        users[str(ctx.author.id)]["last_fish_ounces"] = fish_weight_ounces
        users[str(ctx.author.id)]["last_fish_feet"] = fish_length_feet
        users[str(ctx.author.id)]["last_fish_inches"] = fish_length_inches
        users[str(ctx.author.id)]["last_fish_class"] = fish_class

    # Assign best fish
    async def assign_best(
        self,
        ctx,
        users,
        fish_weight_pounds,
        fish_weight_ounces,
        fish_length_feet,
        fish_length_inches,
        fish_class,
        fish_current,
    ):
        users[str(ctx.author.id)]["best_fish_name"] = fish_current
        users[str(ctx.author.id)]["best_fish_pounds"] = fish_weight_pounds
        users[str(ctx.author.id)]["best_fish_ounces"] = fish_weight_ounces
        users[str(ctx.author.id)]["best_fish_feet"] = fish_length_feet
        users[str(ctx.author.id)]["best_fish_inches"] = fish_length_inches
        users[str(ctx.author.id)]["best_fish_class"] = fish_class

    # Cast fails
    async def cast_fail(self, ctx):
        if ctx.message.guild.id == 735601308597485578:  # respecc regg
            await ctx.send("They ain't bitin... " + "<:FeelsBadMan:795882501028577280>")
        elif ctx.message.guild.id == 696557815959126126:  # Nick's Cursed E-House
            await ctx.send("They ain't bitin... " + "<:FeelsBadMan:820364702830821406>")

    # Total fish doesn't meet requirement
    async def cast_break(self, ctx):
        if ctx.message.guild.id == 735601308597485578:  # respecc regg
            await ctx.send(
                "Something broke the line... " + "<:monkaS:795881948689334292>"
            )
        elif ctx.message.guild.id == 696557815959126126:  # Nick's Cursed E-House
            await ctx.send(
                "Something broke the line... " + "<:monkaS:820364703083528213>"
            )

    # View stats
    @commands.command()
    async def total(self, ctx):
        if await self.channel_check(ctx) is True:
            await self.create_fisher(ctx.author)
            users = await self.get_fishing_data()
            fish_amt = users[str(ctx.author.id)]["total_fish"]

            if ctx.author.nick == None:
                em = discord.Embed()
                em.add_field(name=f"{ctx.author.name}'s total fish:", value=fish_amt)
            else:
                em = discord.Embed()
                em.add_field(name=f"{ctx.author.nick}'s total fish:", value=fish_amt)

            await ctx.send(embed=em)
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Personal best catch
    @commands.command()
    async def pb(self, ctx):
        if await self.channel_check(ctx) is True:
            await self.create_fisher(ctx.author)
            users = await self.get_fishing_data()
            fish_name = users[str(ctx.author.id)]["best_fish_name"]
            fish_weight_pounds = users[str(ctx.author.id)]["best_fish_pounds"]
            fish_weight_ounces = users[str(ctx.author.id)]["best_fish_ounces"]
            fish_length_feet = users[str(ctx.author.id)]["best_fish_feet"]
            fish_length_inches = users[str(ctx.author.id)]["best_fish_inches"]
            fish_class = users[str(ctx.author.id)]["best_fish_class"]
            new_class = await self.class_check(ctx, fish_class)

            if ctx.author.nick == None:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s Best Catch:", color=discord.Color.blue()
                )
                em.add_field(name=f"Fish:", value=fish_name, inline=False)
                em.add_field(
                    name=f"Weight:",
                    value=f"{fish_weight_pounds} pounds and {fish_weight_ounces} ounces",
                    inline=False,
                )
                em.add_field(
                    name=f"Size:",
                    value=f"{fish_length_feet} feet and {fish_length_inches} inches",
                    inline=False,
                )
                em.add_field(name=f"Class:", value=new_class, inline=False)
            else:
                em = discord.Embed(
                    title=f"{ctx.author.nick}'s Best Catch:", color=discord.Color.blue()
                )
                em.add_field(name=f"Fish:", value=fish_name, inline=False)
                em.add_field(
                    name=f"Weight:",
                    value=f"{fish_weight_pounds} pounds and {fish_weight_ounces} ounces",
                    inline=False,
                )
                em.add_field(
                    name=f"Size:",
                    value=f"{fish_length_feet} feet and {fish_length_inches} inches",
                    inline=False,
                )
                em.add_field(name=f"Class:", value=new_class, inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Last fish caught
    @commands.command()
    async def last(self, ctx):
        if await self.channel_check(ctx) is True:
            await self.create_fisher(ctx)
            users = await self.get_fishing_data()
            fish_name = users[str(ctx.author.id)]["last_fish_name"]
            fish_weight_pounds = users[str(ctx.author.id)]["last_fish_pounds"]
            fish_weight_ounces = users[str(ctx.author.id)]["last_fish_ounces"]
            fish_length_feet = users[str(ctx.author.id)]["last_fish_feet"]
            fish_length_inches = users[str(ctx.author.id)]["last_fish_inches"]
            fish_class = users[str(ctx.author.id)]["last_fish_class"]
            new_class = await self.class_check(ctx, fish_class)

            if ctx.author.nick == None:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s Last Catch:", color=discord.Color.blue()
                )
                em.add_field(name=f"Fish:", value=fish_name, inline=False)
                em.add_field(
                    name=f"Weight:",
                    value=f"{fish_weight_pounds} pounds and {fish_weight_ounces} ounces",
                    inline=False,
                )
                em.add_field(
                    name=f"Size:",
                    value=f"{fish_length_feet} feet and {fish_length_inches} inches",
                    inline=False,
                )
                em.add_field(name=f"Class:", value=new_class, inline=False)
            else:
                em = discord.Embed(
                    title=f"{ctx.author.nick}'s Last Catch:", color=discord.Color.blue()
                )
                em.add_field(name=f"Name:", value=fish_name, inline=False)
                em.add_field(
                    name=f"Weight:",
                    value=f"{fish_weight_pounds} pounds and {fish_weight_ounces} ounces",
                    inline=False,
                )
                em.add_field(
                    name=f"Size:",
                    value=f"{fish_length_feet} feet and {fish_length_inches} inches",
                    inline=False,
                )
                em.add_field(name=f"Class:", value=new_class, inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Add fishers to list
    async def create_fisher(self, context):
        case = True
        users = await self.get_fishing_data()
        async for member in context.guild.fetch_members(limit=None):
            if str(member.id) in users:
                case = True
            else:
                users[str(member.id)] = {}
                users[str(member.id)]["username"] = str(member)
                users[str(member.id)]["total_fish"] = 0
                users[str(member.id)]["last_fish_name"] = ""
                users[str(member.id)]["last_fish_pounds"] = 0
                users[str(member.id)]["last_fish_ounces"] = 0
                users[str(member.id)]["last_fish_feet"] = 0
                users[str(member.id)]["last_fish_inches"] = 0
                users[str(member.id)]["last_fish_class"] = 0
                users[str(member.id)]["best_fish_name"] = ""
                users[str(member.id)]["best_fish_pounds"] = 0
                users[str(member.id)]["best_fish_ounces"] = 0
                users[str(member.id)]["best_fish_feet"] = 0
                users[str(member.id)]["best_fish_inches"] = 0
                users[str(member.id)]["best_fish_class"] = 99

            with open("./json/fishing.json", "w") as f:
                json.dump(users, f, indent=4)
            case = False

    # Show list of classes
    @commands.command()
    async def classes(self, ctx):
        if await self.channel_check(ctx) is True:
            cmds = [
                "```Junk: Garbage lying deep within the ocean. Maybe something interesting is down there.",
                "\nSmall: Small fishies. Might not be a fish.",
                "\nMedium: The average sized fish.",
                "\nLarge: Larger than the average sized fish. Kind of heavy to hold.",
                "\nGrand: Overgrown bois, could probably eat you."
                "\nNote: You must catch a total of 100 fish to catch a Grand fish.",
                "\nMassive: Behemoths of the seas, only a skilled fisherman can reel these giants in."
                "\nNote: Not implemented yet...",
                "\nDivine: Ancient myth beings said to roam the deepest parts of the world. Some have even referred to them as gods."
                "\nNote: Not implemented yet...```",
            ]
            await ctx.send("\n".join(cmds))
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Get best fish in server
    @commands.command()
    async def best(self, ctx):
        if await self.channel_check(ctx) is True:
            users = await self.get_fishing_data()
            best_id = str(ctx.author.id)
            user_name = users[str(ctx.author.id)]["username"]
            best_name = users[str(ctx.author.id)]["best_fish_name"]
            best_pounds = users[str(ctx.author.id)]["best_fish_pounds"]
            best_ounces = users[str(ctx.author.id)]["best_fish_ounces"]
            best_feet = users[str(ctx.author.id)]["best_fish_feet"]
            best_inches = users[str(ctx.author.id)]["best_fish_inches"]
            best_class = users[str(ctx.author.id)]["best_fish_class"]
            async for member in ctx.guild.fetch_members(limit=None):
                if users[str(member.id)]["best_fish_class"] < best_class:
                    best_id = str(member.id)
                    user_name = users[str(member.id)]["username"]
                    best_name = users[str(member.id)]["best_fish_name"]
                    best_pounds = users[str(member.id)]["best_fish_pounds"]
                    best_ounces = users[str(member.id)]["best_fish_ounces"]
                    best_feet = users[str(member.id)]["best_fish_feet"]
                    best_inches = users[str(member.id)]["best_fish_inches"]
                    best_class = users[str(member.id)]["best_fish_class"]
                elif users[str(member.id)]["best_fish_class"] == best_class:
                    if users[str(member.id)]["best_fish_pounds"] > best_pounds:
                        best_id = str(member.id)
                        user_name = users[str(member.id)]["username"]
                        best_name = users[str(member.id)]["best_fish_name"]
                        best_pounds = users[str(member.id)]["best_fish_pounds"]
                        best_ounces = users[str(member.id)]["best_fish_ounces"]
                        best_feet = users[str(member.id)]["best_fish_feet"]
                        best_inches = users[str(member.id)]["best_fish_inches"]
                        best_class = users[str(member.id)]["best_fish_class"]
                    elif users[str(member.id)]["best_fish_pounds"] == best_pounds:
                        if users[str(member.id)]["best_fish_ounces"] > best_ounces:
                            best_id = str(member.id)
                            user_name = users[str(member.id)]["username"]
                            best_name = users[str(member.id)]["best_fish_name"]
                            best_pounds = users[str(member.id)]["best_fish_pounds"]
                            best_ounces = users[str(member.id)]["best_fish_ounces"]
                            best_feet = users[str(member.id)]["best_fish_feet"]
                            best_inches = users[str(member.id)]["best_fish_inches"]
                            best_class = users[str(member.id)]["best_fish_class"]

            new_class = await self.class_check(ctx, best_class)
            em = discord.Embed(
                title="Best Fish Ever Caught:", color=discord.Color.blue()
            )
            em.add_field(name=f"Fisher:", value=user_name, inline=False)
            em.add_field(name=f"Fish:", value=best_name, inline=False)
            em.add_field(
                name=f"Weight:",
                value=f"{best_pounds} pounds and {best_ounces} ounces",
                inline=False,
            )
            em.add_field(
                name=f"Size:",
                value=f"{best_feet} feet and {best_inches} inches",
                inline=False,
            )
            em.add_field(name=f"Class:", value=new_class, inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send(
                f"Hey dummy put that command in the berd bot channel."
            )

    # Get fishing info
    async def get_fishing_data(self):
        with open("./json/fishing.json", "r") as f:
            users = json.load(f)
        return users

    # Check the fish classes
    async def class_check(self, ctx, fish_class):
        if fish_class == 7:
            return "Junk"
        elif fish_class == 6:
            return "Small"
        elif fish_class == 5:
            return "Medium"
        elif fish_class == 4:
            return "Large"
        elif fish_class == 3:
            return "Grand"
        elif fish_class == 2:
            return "Massive"
        elif fish_class == 1:
            return "Godlike"

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
    client.add_cog(Fishing(client))
