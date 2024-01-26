# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:56:41 2021

@author: Tilman
"""

import discord
from discord.ext import commands
import asyncio
import sys
import os
import random
from discord import ChannelType
import wave
import textwrap
import matplotlib.mathtext as mathtext
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
from PIL import Image

with open("/home/pi/walross_bot/facts.txt", "r", encoding='utf-8') as f:
    facts=f.readlines()
coin=["Kopf", "Zahl"]

class Commands(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("{} nimmt Befehle entgegen!".format(self.client.user.name))
        
        
    @commands.command()

    async def fact(self, ctx):
        text = random.choice(facts)
        
        if len(text)<2000:
            
            await ctx.send(text)
            
        else:
        
            for line in textwrap.wrap(text, 2000):
                await asyncio.sleep(1)
                await ctx.send(line)
            
    @commands.command()
    async def flip(self, ctx):
        await ctx.send('Ich entscheide mich für '+random.choice(coin))
        
    @commands.command()
    async def join(self, ctx):
        c = ctx.author.voice
        if c!=None:
            await c.channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        c = ctx.author.voice
        if c!=None:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def notfallwalross(self, ctx): 
        path="/home/pi/walross_bot/pics/"+random.choice(os.listdir("/home/pi/walross_bot/pics"))
        with open(path, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=discord.File(path))
            
    @commands.command()
    async def playback(self, ctx):
        
        await ctx.message.delete()
        
        with open('/home/pi/walross_bot/voicerecords/voice.pcm', 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open("voice2"+'.wav', 'wb') as wavfile:
            wavfile.setparams((2, 2, 48000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)
            
        voice_channel_list = ctx.guild.voice_channels

        for channel in voice_channel_list:
            if len(channel.members) != 0:
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="voice2.wav"))
                while vc.is_playing():
                    await asyncio.sleep(0.8)
                await vc.disconnect()
                
    @commands.command()
    async def say(self, ctx):
        
        await ctx.message.delete()
        
        with open('/home/pi/walross_bot/voicerecords/voice.pcm', 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open("/home/pi/walross_bot/voice2"+'.wav', 'wb') as wavfile:
            wavfile.setparams((2, 2, 48000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)

        voice_channel = ctx.message.author.voice

        if voice_channel != None:
            vc = await voice_channel.channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="/home/pi/walross_bot/voice2.wav"))
            while vc.is_playing():
                await asyncio.sleep(0.8)
            await vc.disconnect()
                
    @commands.command()
    async def startrecording(self, ctx):   
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="Recording")
        await ctx.author.add_roles(role)
        
    @commands.command()
    async def f(self, ctx, *args):
        
        

        msg = r' '.join(args)
        
        if msg.count('_')>1:
        
            msgnew = msg.replace('_', '\_')
            await ctx.message.delete()
            await ctx.channel.send(f'{ctx.message.author.mention}: w!f '+msgnew)
            
        offset = "0cm,0cm"
        dvi = r"-T %s -D %d -bg %s -fg %s -O %s" % (
            'tight', 200, 'Transparent', 'White', offset)
        dvioptions = dvi.split()
        
        try:
        
            sp.preview(r'$$'+msg+'$$', viewer='file', filename='/home/pi/walross_bot/formel.png', euler=False,dvioptions=dvioptions)   

            await ctx.send(file=discord.File('/home/pi/walross_bot/formel.png'))
            
        except:
            
            await ctx.channel.send('Nope, das ist zu unverständlich für ein einfaches Walross :confused: ')

            
    @commands.command()
    async def p(self, ctx, *args):
        
        

        msg = r' '.join(args)
        
        if msg.count('_')>1 or msg.count('*')>1:
        
            msgnew = msg.replace('_', '\_')
            msgnew = msg.replace('*', '\*')
            await ctx.message.delete()
            await ctx.channel.send(f'{ctx.message.author.mention}: w!p '+msgnew)
            
def setup(client):
    client.add_cog(Commands(client))