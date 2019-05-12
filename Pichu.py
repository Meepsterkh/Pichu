
from discord.ext.commands import Bot
from discord import Game
import discord
import random
import requests
import time
import os


# def main settings
prefix = ("|")

# change main settings
client = Bot(command_prefix=prefix)
client.remove_command("help")


# Program start up
@client.event
async def on_ready():
    await client.change_presence(game = Game(name = "with Ganondorf"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# function class
class messageFun():
    def __init__(self, message):
        self.message = message

    #url decrease
    def url(self, strings : str, additive = ""):
        url = strings + additive
        response = requests.get(url)
        return(response.json())

    #Dad joke Api
    async def dadJoke(self):
        value = self.url("https://icanhazdadjoke.com/slack")["attachments"][0]["text"]
        await client.send_message(self.message.channel, value)


class SmashFn():
    def __init__(self, message):
        self.message = message
        self.died = False

    async def reset(self):
        for i in range(100):
            for i in self.message.server.roles:
                if(str(i)[-1] == "%"):
                    await client.delete_role(self.message.server, i)

        await client.create_role(self.message.server, name = "0%", colour = discord.Colour(0xffffff))
        await client.send_message(self.message.channel, "Type \"|join\" to play!")

    async def attack(self, percentChange: int, growth: int, base: int):
        for member in self.message.server.members:
            await client.wait_until_ready()
            if(self.check()):
                if (str(self.message.content[-19:-1]) == str(member.id)):
                    roles = discord.utils.get(self.message.server.members, name=member.name).roles
                    for i in roles:
                        roleSpill = str(i).split()
                        if(roleSpill[0][-1] == "%"):
                            percent = int(roleSpill[0][:-1])
                            await client.remove_roles(member, i)

                            if (percent + percentChange >= 120):
                                colours = discord.Colour(0x660000)
                            elif (percent + percentChange >= 100):
                                colours = discord.Colour(0xCB0000)
                            elif (percent + percentChange >= 80):
                                colours = discord.Colour(0xD53333)
                            elif (percent + percentChange >= 65):
                                colours = discord.Colour(0xDF6666)
                            elif(percent + percentChange >= 40):
                                colours = discord.Colour(0xEA9999)
                            elif(percent + percentChange >= 25):
                                colours = discord.Colour(0xF4CCCC)
                            else:
                                colours = discord.Colour(0xFFFFFF)

                            numStr = str(percent + percentChange) + "%"

                            does = False
                            for i in self.message.server.roles:
                                if(i != numStr):
                                    does = True
                            if(does):
                                await client.create_role(self.message.server, name=numStr, colour = colours)

                            await client.wait_until_ready()
                            rolePercent = discord.utils.get(self.message.server.roles, name=numStr)
                            await client.add_roles(member, rolePercent)

                            await self.death(member, percent + percentChange, growth, base)
                            if(self.died == False):
                                await client.send_message(self.message.channel, str(member.name) + " now has " + numStr)
                                self.died = False

    def check(self):
        roles = discord.utils.get(self.message.server.members, name=self.message.author.name).roles
        for i in roles:
            roleSpill = str(i).split()
            if (roleSpill[0][-1] == "%"):
                return True

    async def death(self, member, percent, growth, base):
        total = (percent * growth) + (base * 10)

        if(total >= 10000):
            await client.send_message(self.message.channel, str(member.name) + " died at " + str(percent) + "%")
            rolePercent = discord.utils.get(self.message.server.roles, name=str(percent) + "%")
            await client.remove_roles(member, rolePercent)
            rolePercent = discord.utils.get(self.message.server.roles, name='0%')
            await client.add_roles(member, rolePercent)
            self.died = True

    async def Turn(self):
        for member in self.message.server.members:
            roles = discord.utils.get(self.message.server.members, name=member.name).roles
            for i in roles:
                roleSpill = str(i).split()
                if(roleSpill[0][-1] == "%"):
                    continue
                else:
                    await client.wait_until_ready()
                    rolePercent = discord.utils.get(self.message.server.roles, name='0%')
                    await client.add_roles(self.message.author, rolePercent)
                    await client.delete_message(self.message)
                    await client.send_message(self.message.channel, str(self.message.author) + "has joined the game!")

    async def Start(self):

        await client.send_message(self.message.channel, "The players are:")
        for member in self.message.server.members:
            await client.wait_until_ready()
            roles = discord.utils.get(self.message.server.members, name=member.name).roles
            for i in roles:
                roleSpill = str(i).split()
                if(roleSpill[0][-1] == "%"):
                    await client.send_message(self.message.channel, str(member))





#turn[0], 3 stocks


@client.event
async def on_message(message):
    extra = messageFun(message)
    Smash = SmashFn(message)

    # Debug.Log Text Info
    print(message.author)
    print(message.content)

    # bot replying to self stops
    if message.author == client.user:
        return


    #Hello
    if message.content.startswith('|hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    #Beese Churger
    elif message.content.startswith('beese churger'):
        await client.delete_message(message)
        await client.send_message(message.channel, "Welcome to Mcdownald's \n Do you want a phucking \n Beese Churger?")

    #Jokes
    if message.content.startswith("|joke"):
        await extra.dadJoke()


    if(str(message.author) == "Itchymitchy11#5914"):
        await client.send_message(message.channel, "THUNDERBOLT")


    if (message.content.startswith("|reset")):
        await Smash.reset()

    if (message.content.startswith("|falcon punch")):
        await Smash.attack(27, 100, 1)

    if (message.content.startswith("|ce")):
        await Smash.attack(15, 100, 60)

    if (message.content.startswith("|test")):
        role = discord.utils.get(message.server.roles, name=message.content[6:])
        print(role.position)


    if (message.content.startswith("|join")):
        await Smash.Turn()

    if (message.content.startswith("|start")):
        await Smash.Start()


client.run(str(os.environ.get('BOT_TOKEN')))
