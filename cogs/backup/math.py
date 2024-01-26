# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 18:20:46 2021

@author: Tilman
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:50:30 2021

@author: Tilman
"""

import discord
from discord.ext import commands
import asyncio
import re
import ast
import numpy as np
import matplotlib.pyplot as plt

pi=np.pi
e=np.exp(1)

UNARY_OPS = (ast.UAdd, ast.USub)
BINARY_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow)

class Math(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.id != message.author.id:

            if 'y=' in message.content.lower():
                new_message = message.content.lower()
                new_message = new_message.replace('y=','')
                y = rangeextract(new_message)
                temp = subs(y[0]).rstrip()
                if check(temp):
                    try:
                        discordplot(temp,y[1])
                        await message.channel.send(file=discord.File('/home/pi/walross_bot/plot.png'))
                    except:
                        discordplot(temp,y[1])
                        await message.channel.send(file=discord.File('/home/pi/walross_bot/plot.png'))



            elif '+' in message.content.lower() or '-' in message.content.lower() or '*' in message.content.lower() or '/' in message.content.lower() or '^' in message.content.lower() or '!' in message.content.lower() or 'sin' in message.content.lower() or 'cos' in message.content.lower() or 'tan' in message.content.lower() or 'log' in message.content.lower() or 'ln' in message.content.lower() or 'pi' in message.content.lower():
                new_message = message.content.lower()
                new_message = subs(new_message)
                if check(new_message):
                    await message.channel.send(eval(new_message))
                else:
                    pass



              
                             
def is_arithmetic(s):
    def _is_arithmetic(node):
        if isinstance(node, ast.Num):
            return True
        elif isinstance(node, ast.Expression):
            return _is_arithmetic(node.body)
        elif isinstance(node, ast.UnaryOp):
            valid_op = isinstance(node.op, UNARY_OPS)
            return valid_op and _is_arithmetic(node.operand)
        elif isinstance(node, ast.BinOp):
            valid_op = isinstance(node.op, BINARY_OPS)
            return valid_op and _is_arithmetic(node.left) and _is_arithmetic(node.right)
        else:
            raise ValueError('Unsupported type {}'.format(node))

    try:
        return _is_arithmetic(ast.parse(s, mode='eval'))
    except (SyntaxError, ValueError):
        return False
    
def abschange(s,abfuncname='np.abs'):
    s.replace('abs','np.abs')
    pos =s.find('|')
    while pos >=0:
        #s=s[:pos] + s[pos+1:]
        

        klam=0
        abses=1
        spos=pos+1 #Suchposition
        found=False
        while not(found) and spos<len(s)-1: #sucht das gegenstück zu dem Betragsstrich
            spos+=1
            if s[spos]==')':
                klam-=1
            elif s[spos]=='(':
                klam+=1
            elif s[spos]=='|' and klam==0:
                
                
                if re.match('[\*\+\-/%\^]',s[spos-1]):
                    #klam+=1
                    abses+=1
                else:
                    abses-=1
                    if abses==0:found=True
        if (not(found)): raise ValueError( "Invalid absolutum expression")
                    
        s=s[:pos]+abfuncname+'('+s[pos+1:spos]+')'+s[spos+1:]
            
        pos =s.find('|')
      
    return s    

def fakchange(s,fakfunctionname='np.math.factorial'):
    pos =s.find('!')
    while pos >=0:
        s=s[:pos] + s[pos+1:]
        
        if pos-1<0:
            raise "Invalid Factorial Expression"
        elif s[pos-1]==')':
            klam=-1
            spos=pos-1 #Suchposition
            while klam!=0: #sucht das gegenstÃ¼ck zu der geschlossenen Klammer
                spos-=1
                if s[spos]==')':
                    klam-=1
                elif s[spos]=='(':
                    klam+=1
            s=s[:spos]+fakfunctionname+s[spos:]
            
        elif re.match('[0-9]',s[pos-1]): #sucht nach anfang der Zahl
            spos=pos-1 #Suchposition
            while re.match('[0-9]',s[spos]) and spos>=0:
                spos-=1
            s=s[:spos+1]+fakfunctionname+'('+s[spos+1:pos]+')'+s[pos:]
        pos =s.find('!')

    
    return s

def subs(x):
    
    x = re.sub(r"sin", "np.sin", x)
    x = re.sub(r"cos", "np.cos", x)
    x = re.sub(r"tan", "np.tan", x)
    x = re.sub(r"arcsin", "np.arcsin", x)
    x = re.sub(r"arccos", "np.arccos", x)
    x = re.sub(r"arctan", "np.arctan", x)
    x = re.sub(r"log", "np.log10", x)
    x = re.sub(r"ln", "np.log", x)
    x = re.sub(r"abs", "np.abs", x)
    x = re.sub(r"sqrt", "np.sqrt", x)

    x=fakchange(x)
    x=abschange(x)    

    x = x.replace('^', '**')
    return x

def check(y)    :
    
    if y[0]=='e': y=y[2:]
    if y[0:2]=='pi': y=y[3:]
    
    y = re.sub(r"np.sin", "", y)
    y = re.sub(r"np.cos", "", y)
    y = re.sub(r"np.tan", "", y)
    y = re.sub(r"np.arcsin", "", y)
    y = re.sub(r"np.arccos", "", y)
    y = re.sub(r"np.arctan", "", y)
    y = re.sub(r"[/+*-]*e", "3", y)
    y = re.sub(r"[/+*-]*pi", "3", y)
    y = re.sub(r"[/+*-]*x", "3", y)
    y = re.sub(r"np.log", "", y)
    y = re.sub(r"np.log10", "", y)
    y = re.sub(r"np.abs", "", y)
    y = re.sub(r"np.sqrt", "", y)
    y = re.sub(r"np.math.factorial", "", y)
    y = re.sub(r"\(", "", y)
    y = re.sub(r"\)", "", y)
    
    if y:
        return is_arithmetic(y)
    
    else:
        return True

def rangeextract(s):
    match=re.search('\[-?[0-9][0-9]*.?[0-9]*[,\s]*-?[0-9][0-9]*.?[0-9]*\]',s)
    if match:
        rangestr=s[match.span()[0]:match.span()[1]]
        s=s[:match.span()[0]]+s[match.span()[1]:]
        rangestr=rangestr[1:-1]#schneidet die eckigen Klammern weg
        drange=re.split('[,\s]',rangestr)
        drange=[drange[0],drange[-1]]
    else: drange=[-10,10]
    #'\[[0-9][0-9]*.?[0-9]*[,\s][0-9][0-9]*.?[0-9]*\]'
    return s,[float(drange[0]),float(drange[1])]

def discordplot(fstr,drange=None,axcolor='white',linecolor='white'):
    if drange is None: drange=[-10,10]
    x=np.linspace(drange[0],drange[1],100)
    y=eval(fstr)
    if not 'x' in fstr: y = y*np.ones(len(x))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x,y,color=linecolor)
    plt.ylabel('y')
    plt.xlabel('x')
    ax.spines['bottom'].set_color(axcolor)
    ax.spines['top'].set_color([0,0,0,0])
    ax.spines['left'].set_color(axcolor)
    ax.spines['right'].set_color([0,0,0,0])
    ax.xaxis.label.set_color(axcolor)
    ax.tick_params(axis='x', colors=axcolor)
    ax.yaxis.label.set_color(axcolor)
    ax.tick_params(axis='y', colors=axcolor)
    if min(y)<1 and max(y)>1:
        ax.axhline(linewidth=1, linestyle='dashed', color='silver')
    if min(x)<0 and max(x)>0:
        ax.axvline(linewidth=1, linestyle='dashed', color='silver')


    plt.savefig('/home/pi/walross_bot/plot.png',dpi=200,format='png',transparent=True)

def setup(client):
    client.add_cog(Math(client))
    