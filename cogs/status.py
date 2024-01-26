# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:33:54 2021

@author: Tilman
"""

import discord
from discord.ext import commands
import asyncio


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

async def status_task(client):
    while True:
        await client.change_presence(
            activity=discord.Game("gerade nichts"), status=discord.Status.online
        )
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Game("gerne mit Jonas"), status=discord.Status.online
        )
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="dem Meer"
            )
        )
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="anderen Walrossen zu"
            )
        )
        await asyncio.sleep(60)


def setup(client):
    client.add_cog(Status(client))
