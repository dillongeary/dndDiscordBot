import discord
import random

client = discord.Client()
users = {}
initiative = []
position = 0

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

    if discord_message.startswith(";stat"):
        output = ""
        for i in range(6):
            rolls = []
            for j in range(4):
                rolls.append(random.randint(1,6))
            rolls.sort()
            total = rolls[1] + rolls[2] + rolls[3]
            output += str(total)
            if i < 5 :
                output += ", "


        await message.channel.send(output)

    elif discord_message.startswith(";init"):
        initiative = discord_message[6:].split(" ")
        position = 0

    elif discord_message == ";n":
        chanel = client.get_channel(806685016661819482) #rolling
        await chanel.send("Turn: " + str(initiative[position]))
        position+=1
        if position == len(initiative) : position = 0

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#roll

    elif discord_message.startswith(";") and "d" in discord_message:
        try:
            alteredMessage = discord_message[1:].replace("-","+-").split("+")

            output = []
            total = 0
            for i in alteredMessage:
                if "d" in i:
                    numbers = i.split("d")
                    rolls = []
                    if numbers[0] == '': numbers[0] = 1
                    for j in range(int(numbers[0])):
                        roll = random.randint(1, int(numbers[1]))
                        total += roll
                        rolls.append(roll)

                    output.append(rolls)

                else:
                    total += int(i)
                    output.append(int(i))

            big = False
            if len(output) == 1:
                for i in output:
                    if type(i) is list:
                        if len(i) > 1:
                            big = True
            else:
                big = True

            for i in range(len(output)):
                if type(output[i]) is list:
                    element = output[i]
                    element = str(element)
                    element = element.replace("[","")
                    element = element.replace("]","")
                    element = element.replace(","," +")
                    if len(output[i]) > 1 :
                        element += " = " + str(sum(output[i]))
                    output[i] = element

            output = str(output)
            output = output.replace("'","")
            output = output.replace("[","(")
            output = output.replace("]",")")

            if not big:
                await message.channel.send(str(message.author.mention) + " rolled **" + str(total) + "**")
            else:
                await message.channel.send(str(message.author.mention) + " rolled **" + str(total) + "**    " + str(output))
        except:
            print("invalid input")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#advantage

    elif discord_message.startswith("adv;") and "d" in discord_message:
        try:
            alteredMessage = discord_message[4:].replace("-","+-").split("+")

            output1 = []
            total1 = 0
            for i in alteredMessage:
                if "d" in i:
                    numbers = i.split("d")
                    rolls = []
                    if numbers[0] == '': numbers[0] = 1
                    for j in range(int(numbers[0])):
                        roll = random.randint(1, int(numbers[1]))
                        total1 += roll
                        rolls.append(roll)

                    output1.append(rolls)

                else:
                    total1 += int(i)
                    output1.append(int(i))

            output2 = []
            total2 = 0
            for i in alteredMessage:
                if "d" in i:
                    numbers = i.split("d")
                    rolls = []
                    if numbers[0] == '': numbers[0] = 1
                    for j in range(int(numbers[0])):
                        roll = random.randint(1, int(numbers[1]))
                        total2 += roll
                        rolls.append(roll)

                    output2.append(rolls)

                else:
                    total2 += int(i)
                    output2.append(int(i))

            if total1 > total2:
                output = output1
                total = total1
                lowerOutput = output2

            else:
                output = output2
                total = total2
                lowerOutput = output1

            for i in range(len(output)):
                if type(output[i]) is list:
                    element = output[i]
                    element = str(element)
                    element = element.replace("[","")
                    element = element.replace("]","")
                    element = element.replace(","," +")
                    if len(output[i]) > 1 :
                        element += " = " + str(sum(output[i]))
                    output[i] = element

            output = str(output)
            output = output.replace("'","")
            output = output.replace("[","(")
            output = output.replace("]",")")

            for i in range(len(lowerOutput)):
                if type(lowerOutput[i]) is list:
                    element = lowerOutput[i]
                    element = str(element)
                    element = element.replace("[","")
                    element = element.replace("]","")
                    element = element.replace(","," +")
                    if len(lowerOutput[i]) > 1 :
                        element += " = " + str(sum(lowerOutput[i]))
                    lowerOutput[i] = element

            lowerOutput = str(lowerOutput)
            lowerOutput = lowerOutput.replace("'","")
            lowerOutput = lowerOutput.replace("[","(")
            lowerOutput = lowerOutput.replace("]",")")

            await message.channel.send(str(message.author.mention) + " rolled **" + str(total) + "**    " + str(output) + "  " + str(lowerOutput))

        except:
            print("invalid input")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#disadvantage

    elif discord_message.startswith("dis;") and "d" in discord_message:
        try:
            alteredMessage = discord_message[4:].replace("-", "+-").split("+")

            output1 = []
            total1 = 0
            for i in alteredMessage:
                if "d" in i:
                    numbers = i.split("d")
                    rolls = []
                    if numbers[0] == '': numbers[0] = 1
                    for j in range(int(numbers[0])):
                        roll = random.randint(1, int(numbers[1]))
                        total1 += roll
                        rolls.append(roll)

                    output1.append(rolls)

                else:
                    total1 += int(i)
                    output1.append(int(i))

            output2 = []
            total2 = 0
            for i in alteredMessage:
                if "d" in i:
                    numbers = i.split("d")
                    rolls = []
                    if numbers[0] == '': numbers[0] = 1
                    for j in range(int(numbers[0])):
                        roll = random.randint(1, int(numbers[1]))
                        total2 += roll
                        rolls.append(roll)

                    output2.append(rolls)

                else:
                    total2 += int(i)
                    output2.append(int(i))

            if total1 < total2:
                output = output1
                total = total1
                lowerOutput = output2

            else:
                output = output2
                total = total2
                lowerOutput = output1

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

            for i in range(len(lowerOutput)):
                if type(lowerOutput[i]) is list:
                    element = lowerOutput[i]
                    element = str(element)
                    element = element.replace("[", "")
                    element = element.replace("]", "")
                    element = element.replace(",", " +")
                    if len(lowerOutput[i]) > 1:
                        element += " = " + str(sum(lowerOutput[i]))
                    lowerOutput[i] = element

            lowerOutput = str(lowerOutput)
            lowerOutput = lowerOutput.replace("'", "")
            lowerOutput = lowerOutput.replace("[", "(")
            lowerOutput = lowerOutput.replace("]", ")")

            await message.channel.send(
                str(message.author.mention) + " rolled **" + str(total) + "**    " + str(output) + "  " + str(lowerOutput))

        except:
            print("invalid input")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

tokenFile = open("token.txt")
token = tokenFile.read()

client.run(token)