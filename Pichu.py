
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
    def url(self, strings : str, additive = None):
        url = strings + additive
        response = requests.get(url)
        return(response.json())

    #Dad joke Api
    async def dadJoke(self):
        value = self.url("https://icanhazdadjoke.com/slack")["attachments"][0]["text"]
        await client.send_message(self.message.channel, value)


@client.event
async def on_message(message):
    extra = messageFun(message)

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



client.run(str(os.environ.get('BOT_TOKEN'))))
