# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:50:30 2021

@author: Tilman
"""

import discord
from discord.ext import commands
import asyncio

walross_namen = ["walross", "walrosse", "wahlross", "wahlrosse", "walrus", "walros"]
beleidigungen = [
    "dumm",
    "blöd",
    "scheiße",
    "kacke",
    "schlecht",
    "nichtsnutzig",
    "doof",
    "hässlich",
    "schmutzig",
    "hurensöhne",
    "hurensohn",
]


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.id != message.author.id:
            y = False
            for ross in walross_namen:
                if ross in message.content.lower():
                    x = ""
                    y = True
                    nichts = message.content.count("nicht ")
                    for bel in beleidigungen:
                        if bel in message.content.lower():
                            x += bel.upper() + "!!! "
            if y:
                if not x:
                    await message.channel.send("WALROSS 🎉")
                elif nichts % 2 == 0:
                    await message.channel.send(
                        x
                        + "Wie kannst du es wagen, diese majestätischen Kreaturen so zu beleidigen???"
                    )

                    voice_channel = message.author.voice
                    if voice_channel != None:
                        vc = await voice_channel.channel.connect()
                        vc.play(
                            discord.FFmpegPCMAudio(
                                source="/home/pi/walross_bot/walross.mp3"
                            )
                        )
                        while vc.is_playing():
                            await asyncio.sleep(0.4)
                        await vc.disconnect()
                        await message.author.move_to(
                            None, reason="Du hast das Walross beleidigt"
                        )
                elif nichts % 2 == 1:
                    await message.channel.send(
                        'Die Betonung liegt ganz klar auf dem "nicht"!'
                    )

        # await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.client.user.id != member.id and before.channel != None:
            if before.channel.id == 803547586581102595 and not member.bot:
                role = discord.utils.get(member.guild.roles, name="Recording")
                await member.remove_roles(role)


def setup(client):
    client.add_cog(Message(client))
