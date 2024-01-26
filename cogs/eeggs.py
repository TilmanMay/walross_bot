# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 09:41:48 2021

@author: Tilman
"""


import discord
from discord.ext import commands
import asyncio

e69 = ['🇳','🇮','🇨','🇪']
e420 = ['4️⃣', '2️⃣', '0️⃣', '🔥']
ehb = ['🥳']
flip='(╯°□°）╯︵ ┻━┻'
unflip='┬─┬ ノ( ゜-゜ノ)'


class Eeggs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.id != message.author.id:
            if message.content.lower() == flip:
                await message.channel.send(unflip)
            if message.content.lower() == "nein":
                await message.channel.send("Doch!")
            if "69" in message.content.lower():
                for emoji in e69:
                    await message.add_reaction(emoji)
            if "420" in message.content.lower():
                for emoji in e420:
                    await message.add_reaction(emoji)
            if (
                "alles gute" in message.content.lower()
                or "happy bi" in message.content.lower()
            ):
                for emoji in ehb:
                    await message.add_reaction(emoji)
        await self.client.process_commands(message)

def setup(client):
    client.add_cog(Eeggs(client))
