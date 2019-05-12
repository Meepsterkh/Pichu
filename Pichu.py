
from discord.ext.commands import Bot
from discord import Game
import discord
import random
import requests
import os
import time


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

        await client.create_role(self.message.server, name = "0%")
        rolePercent = discord.utils.get(self.message.server.roles, name='0%')
        for member in self.message.server.members:
            await client.add_roles(member, rolePercent)
        await client.send_message(self.message.channel, "3!")
        time.sleep(.5)
        await client.send_message(self.message.channel, "2!")
        time.sleep(.5)
        await client.send_message(self.message.channel, "1!")
        time.sleep(.5)
        await client.send_message(self.message.channel, "GO!")

    async def attack(self, percentChange: int, growth: int, base: int):
        for member in self.message.server.members:
            if (str(self.message.content[-19:-1]) == str(member.id)):
                roles = discord.utils.get(self.message.server.members, name=member.name).roles
                for i in roles:
                    roleSpill = str(i).split()
                    if(roleSpill[0][-1] == "%"):
                        percent = int(roleSpill[0][:-1])
                        await client.remove_roles(member, i)


                        numStr = str(percent + percentChange) + "%"
                        does = False
                        for i in self.message.server.roles:
                            if(i != numStr):
                                does = True
                        if(does):
                            await client.create_role(self.message.server, name=numStr)

                        await client.wait_until_ready()
                        rolePercent = discord.utils.get(self.message.server.roles, name=numStr)
                        await client.add_roles(member, rolePercent)

                        await self.check(member, percent + percentChange, growth, base)
                        if(self.died == False):
                            await client.send_message(self.message.channel, str(member.name) + " now has " + numStr)
                            self.died = False

    async def check(self, member, percent, growth, base):
        total = (percent * growth) + (base * 25)

        if(total >= 7500):
            await client.send_message(self.message.channel, str(member.name) + " died at " + str(percent) + "%")
            rolePercent = discord.utils.get(self.message.server.roles, name=str(percent) + "%")
            await client.remove_roles(member, rolePercent)
            rolePercent = discord.utils.get(self.message.server.roles, name='0%')
            await client.add_roles(member, rolePercent)
            self.died = True

#turn[0], 3 stocks

#total Knockback == (percent * knockback growth) + base knockback

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

client.run(str(os.environ.get('BOT_TOKEN')))
