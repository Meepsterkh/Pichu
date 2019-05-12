
from discord.ext.commands import Bot
from discord import Game
import discord
import random
import requests
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

    async def reset(self):
        for i in range(100):
            for i in self.message.server.roles:
                if(str(i)[0] == "~"):
                    await client.delete_role(self.message.server, i)

        await client.create_role(self.message.server, name = "~0%")
        rolePercent = discord.utils.get(self.message.server.roles, name='~0%')
        for member in self.message.server.members:
            await client.add_roles(member, rolePercent)
            await client.send_message(self.message.channel, "Game has been Reset, Fight")

    async def attack(self, percentChange: int):
        for member in self.message.server.members:
            if (str(self.message.content[-19:-1]) == str(member.id)):
                roles = discord.utils.get(self.message.server.members, name=member.name).roles
                for i in roles:
                    roleSpill = str(i).split()
                    if(roleSpill[0][0] == "~"):
                        percent = int(roleSpill[0][1:-1])
                        await client.remove_roles(member, i)


                        numStr = "~" + str(percent + percentChange) + "%"
                        does = False
                        for i in self.message.server.roles:
                            if(i != numStr):
                                does = True
                        if(does):
                            await client.create_role(self.message.server, name=numStr)

                        rolePercent = discord.utils.get(self.message.server.roles, name=numStr)
                        await client.add_roles(member, rolePercent)
                        await client.send_message(self.message.channel, str(member.name) + " Now Has " + numStr)



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

    # if(message.content.startswith("|reset")):
    #     for i in range(100):
    #         for i in message.server.roles:
    #             if(str(i)[0] == "~"):
    #                 await client.delete_role(message.server, i)
    #
    #     await client.create_role(message.server, name = "~0%")
    #     rolePercent = discord.utils.get(message.server.roles, name='~0%')
    #     for member in message.server.members:
    #         await client.add_roles(member, rolePercent)

    if (message.content.startswith("|falcon punch")):
        await Smash.attack(27)

    # if(message.content.startswith("|falcon punch")):
    #     for member in message.server.members:
    #         if (str(message.content[16:-1]) == str(member.id)):
    #             roles = discord.utils.get(message.server.members, name=member.name).roles
    #             for i in roles:
    #                 roleSpill = str(i).split()
    #                 if(roleSpill[0][0] == "~"):
    #                     percent = int(roleSpill[0][1:-1])
    #                     await client.remove_roles(member, i)
    #
    #
    #                     numStr = "~" + str(percent + 27) + "%"
    #                     does = False
    #                     for i in message.server.roles:
    #                         if(i != numStr):
    #                             does = True
    #                     if(does):
    #                         await client.create_role(message.server, name=numStr)
    #
    #                     rolePercent = discord.utils.get(message.server.roles, name=numStr)
    #                     await client.add_roles(member, rolePercent)




client.run(str(os.environ.get('BOT_TOKEN')))
