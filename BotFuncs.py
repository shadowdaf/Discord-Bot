# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:56:05 2020

@author: Dafydd
"""
from datetime import datetime as dt
from mcstatus import MinecraftServer
import discord

def getMembers(guild):
    membs = {}
    membList = []
    for m in guild.members:
        discordID = str(m.name)+"#"+str(m.discriminator)
        #print(discordID)
        membs[discordID] = m.id
        membList.append(discordID)
    return membs, membList

def getVoiceChannels(guild):
    chans = {}
    for vc in guild.voice_channels:
        chans[vc.name] = vc.id
    return chans

def get_user_vc(guild, user):
    chan = False
    membs, membList = getMembers(guild)
    target = guild.get_member(membs[user])
    for vc in guild.voice_channels:
        if target in vc.members:
            chan = vc
            break
    return chan

def getRoles(guild):
    roles = {}
    for r in guild.roles:
        roles[r.name] = r
        
    return roles

def user2name(user):
    name = user.name
    disc = user.discriminator
    discordid = str(name)+"#"+str(disc)
    return discordid

def make_time(timestring):
    format = 0
    if 'h' in timestring:
        format += 1
    if 'm' in timestring:
        format += 10
    if 's' in timestring:
        format +=100
    
    return

def get_mc_status(ip):
    #check for valid ip
    if len(ip.split(":")) == 2:
        ip = str(ip)
    elif len(ip.split(":")) == 1:
        ip = str(ip) + ":25565"
    else:
        return {"status":-1}
    
    server = MinecraftServer.lookup(ip)
    try:
        dets = server.status()
        out = {"status":1,
               "colour":discord.Colour.green(),
               "title":"Minecraft Server Status",
               "description":"Server {0} at {1} is Online\nPlayers : {2}/{3}".format(dets.description['text'],ip,dets.players.online,dets.players.max)}
    except:
        out = {"status":0,
               "colour":discord.Colour.red(),
               "title":"Minecraft Server Status",
               "description":"Server at {0} is currently offline!".format(ip)}
    return out

        
    