# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:29:51 2021

@author: Tilman
"""

import discord
from discord.ext import commands
import os


client = commands.Bot(command_prefix=["w!", "W!"])


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    print("loaded " + extension)


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print("unloaded " + extension)


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    print("reloaded " + extension)


for filename in os.listdir("/home/pi/walross_bot/cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("Hier würde ein Token stehen")
