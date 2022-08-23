# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:56:05 2020

@author: Dafydd
"""
from datetime import datetime as dt
from mcstatus import JavaServer
from mcrcon import MCRcon
import dateparser as dp
import time,discord,aiocsv,aiofiles,asyncio

def find_jim(guild):
    for m in guild.members:
        if m.name == "Jimbob" and m.discriminator == "9284":
            jim = m
            break
    return jim


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

def get_tickrate(ip,rconpassword):
    try:
        with MCRcon(ip,rconpassword) as mcr:
            resp = mcr.command("/tps")
        #print(resp)
            mcr.disconnect()
        tps = resp
        """
            
        dummy = resp.split("TPS") 
        tps = [dummy[0].strip()]
        for i in dummy:
            loc = i.find(")")+1
            if (loc):
                tps.append(i[loc:])
        tps = tps[:-1]
        """
    except:
        tps = ["Unable to access tps information"]

    
    
    
    return tps

def get_mc_status(ip):
    #check for valid ip
    if len(ip.split(":")) == 2:
        ip = str(ip)
    elif len(ip.split(":")) == 1:
        ip = str(ip) + ":25565"
    else:
        return {"status":-1}
    server = JavaServer.lookup(ip)
    try:
        dets = server.status()
        out = {"status":1,
               "colour":discord.Colour.green(),
               "title":"Minecraft Server Status",
               "description":"Server {0} at {1} is Online\nPlayers Online : {2}/{3}".format(dets.description,ip,dets.players.online,dets.players.max)}
        try:
            players = server.query().players.names
            out["players"] = players
        except:
            print("Server Query is disabled on {0}".format(ip))

    except:
        out = {"status":0,
               "colour":discord.Colour.red(),
               "title":"Minecraft Server Status",
               "description":"Server at {0} is currently offline!".format(ip)}
    return out

def get_unix_time(intime):
    """
    Takes a date and time and converts to unix time
    """
    intime = "le "+intime
    dtime = dp.parse(intime)
    utime = int(time.mktime(dtime.timetuple()))
    
    
    return utime
    

async def backup_user_nicknames(guild):
    """
    Backs up the nicknames of the guild and stores the file as {guild}.csv
    """
    backup_success = False
    async with aiofiles.open("{0}.csv".format(guild), mode="w", encoding="utf-8",newline="") as afp:
        writer = aiocsv.AsyncWriter(afp, dialect="unix")
        for m in guild.members:
            await writer.writerow([str(m.id),"{0}#{1}".format(m.name,m.discriminator),m.nick])
    backup_success = True
    

    return backup_success

def get_current_time():
    now = dt.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


        
    