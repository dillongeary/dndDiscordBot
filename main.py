import discord
import random
import asyncio
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

client = discord.Client()
users = {}
initiative = []
position = 0


def output_cleanup(output):
    for i in range(len(output)):
        if type(output[i]) is list:
            element = output[i]
            element = str(element)
            element = element.replace("[", "")
            element = element.replace("]", "")
            element = element.replace(",", " +")
            if len(output[i]) > 1:
                element += " = " + str(sum(output[i]))
            output[i] = element



    output = str(output)
    output = output.replace("'", "")
    output = output.replace("[", "(")
    output = output.replace("]", ")")

    return output


def dice_roller(alteredMessage):
    output = []
    total = 0
    for i in alteredMessage:  # altered message = list of each command
        if "d" in i:  # if command is a rolly one
            numbers = i.split("d")  # separate amount of dice and number of faces
            rolls = []  # output rolls
            if numbers[0] == '': numbers[0] = 1  # changes a d20 to a 1d20
            for j in range(int(numbers[0])):  # loop the amount of die we have
                roll = random.randint(1, int(numbers[1]))
                total += roll
                rolls.append(roll)

            output.append(rolls)

        else:
            total += int(i)
            output.append(int(i))
    output.append(total)
    return output


async def rolling_command(discord_message, message):
    try:
        alteredMessage = discord_message[1:].replace("-", "+-").split("+")

        output = dice_roller(alteredMessage)
        total = output.pop()

        big = False
        if len(output) == 1:
            for i in output:
                if type(i) is list:
                    if len(i) > 1:
                        big = True
        else:
            big = True

        if big:
            output = output_cleanup(output)

        if not big:
            await message.channel.send(str(message.author.mention) + " rolled **" + str(total) + "**")
        else:
            await message.channel.send(str(message.author.mention) + " rolled **" + str(total) + "**    " + str(output))
    except:
        print("invalid input")


def stats(): #generate a random statblock
    output = ""
    for i in range(6):
        rolls = []
        for j in range(4):
            rolls.append(random.randint(1, 6))
        rolls.sort()
        total = rolls[1] + rolls[2] + rolls[3]
        output += str(total)
        if i < 5:
            output += ", "

    return output

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Game(name='Dungeons and Dragons')
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    discord_message = message.content.lower()

    global initiative
    global position

    #----------------------------------------------

    #stat generator

    if discord_message.startswith(";stat"):
        await message.channel.send(stats())

    #initiative tracker

    elif discord_message.startswith(";init"):
        initiative = discord_message[6:].split(" ")
        position = 0

    elif discord_message == ";n":
        chanel = client.get_channel(806685016661819482)
        await chanel.send("Turn: " + str(initiative[position]))
        position+=1
        if position == len(initiative) : position = 0

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #roll dice

    elif discord_message.startswith(";") and "d" in discord_message:
        await rolling_command(discord_message, message)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #advantage

    elif discord_message.startswith("adv;") and "d" in discord_message:
        try:
            alteredMessage = discord_message[4:].replace("-","+-").split("+")

            output1 = dice_roller(alteredMessage)
            total1 = output1.pop()
            output1 = output_cleanup(output1)

            output2 = dice_roller(alteredMessage)
            total2 = output2.pop()
            output2 = output_cleanup(output2)

            if total1 > total2:
                print("first")
                await message.channel.send(str(message.author.mention) + " rolled **" + str(total1) + "**    " + str(output1) + "  ~~" + str(output2) + "~~")
            else:
                print("second)")
                await message.channel.send(str(message.author.mention) + " rolled **" + str(total2) + "**    " + str(output2) + "  ~~" + str(output1) + "~~")
        except:
            print("invalid input")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #disadvantage

    elif discord_message.startswith("dis;") and "d" in discord_message:
        try:
            alteredMessage = discord_message[4:].replace("-", "+-").split("+")

            output1 = dice_roller(alteredMessage)
            total1 = output1.pop()
            output1 = output_cleanup(output1)

            output2 = dice_roller(alteredMessage)
            total2 = output2.pop()
            output2 = output_cleanup(output2)

            if total1 < total2:
                await message.channel.send(
                    str(message.author.mention) + " rolled **" + str(total1) + "**    " + str(output1) + "  ~~" + str(
                        output2) + "~~"
                )

            else:
                await message.channel.send(
                    str(message.author.mention) + " rolled **" + str(total2) + "**    " + str(output2) + "  ~~" + str(
                        output1) + "~~"
                )

        except:
            print("invalid input")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #slash commands

slash = SlashCommand(client, sync_commands=True)

guild_ids = [869302998453583913,806249213095968806,845056122461487154]

@slash.slash(name="stats",
             description="Roll for stats!",
             guild_ids=guild_ids
             )
async def _stats(ctx):
    message = await ctx.send("Rolling...")
    await asyncio.sleep(5)
    await message.edit(content=str(stats()))


stealth_stats = {
    331780916584382485: 5, #dillon
    312672250161659915: 1, #ewan
    581107203092643840: 8, #megan
    580016038570360842: 7, #amelia
    758692942696546335: 1, #byron
}

perception_stats = {
    331780916584382485: 4, #dillon
    312672250161659915: 1, #ewan
    581107203092643840: 7, #megan
    580016038570360842: 5, #amelia
    758692942696546335: 0, #byron
}

initiative_stats = {
    331780916584382485: 2, #dillon
    312672250161659915: 1, #ewan
    581107203092643840: 4, #megan
    580016038570360842: 4, #amelia
    758692942696546335: 1, #byron
}

stat_dict = {
    "stealth": stealth_stats,
    "perception": perception_stats,
    "initiative": initiative_stats
}

async def slash_rolls(ctx, id, dict):
    try:
        dict = stat_dict.get(dict)
        if id == 580016038570360842 and dict == stealth_stats: #have different rules for those who have disadvantage
            value1 = random.randint(1,20)
            value2 = random.randint(1,20)
            if value1 < value2:
                await ctx.send("<@" + str(id) + "> rolled **" + str(value1 + dict.get(id)) + "**   (" + str(value1) + " + " + str(dict.get(id)) + ")  ~~(" + str(value2) + " + " + str(dict.get(id)) + ")~~")
            else:
                await ctx.send(
                    "<@" + str(id) + "> rolled **" + str(value2 + dict.get(id)) + "**   (" + str(value2) + " + " + str(
                        dict.get(id)) + ")  ~~(" + str(value1) + " + " + str(dict.get(id)) + ")~~")
        elif id in dict.keys():
            value = random.randint(1, 20)
            await ctx.send("<@" + str(id) + "> rolled **" + str(value + dict.get(id)) + "**   (" + str(value) + " + " + str(dict.get(id)) + ")")
    except:
        print("slash rolls - invalid id:\n" + id)


@slash.slash(name="stealth",
             description="Roll a steath roll!",
             guild_ids=guild_ids
             )
async def stealth(ctx):
    if str(ctx.author.id) == "236915098289963010": #for if the DM was to ask for stealth
        for i in initiative_stats.keys():
            await slash_rolls(ctx, i, "stealth") #display everyones stealth
    else:
        await slash_rolls(ctx, ctx.author.id, "stealth")


@slash.slash(name="perception",
             description="Roll a perception roll!",
             guild_ids=guild_ids
             )
async def perception(ctx):
    if str(ctx.author.id) == "236915098289963010": #for if the DM was to ask for perception
        for i in initiative_stats.keys():
            await slash_rolls(ctx, i, "perception") #display everyones perception
    else:
        await slash_rolls(ctx, ctx.author.id, "perception")


@slash.slash(name="initiative",
             description="Roll an initiative roll!",
             guild_ids=guild_ids
             )

async def initiative(ctx):
    if str(ctx.author.id) == "236915098289963010": #for if the DM was to ask for initiative
        for i in initiative_stats.keys():
            await slash_rolls(ctx, i, "initiative") #display everyones initiative
    else:
        await slash_rolls(ctx, ctx.author.id, "initiative")

tokenFile = open("token.txt")
token = tokenFile.read()

client.run(token)