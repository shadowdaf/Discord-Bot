# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:03:32 2020

@author: Dafydd
"""
import nest_asyncio,asyncio,aiofiles,aiocsv
nest_asyncio.apply()

import discord,os,logging,datetime
from discord.ext import commands
from dotenv import load_dotenv
import BotFuncs as BF
from mutagen.mp3 import MP3

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN').strip('{').strip('}')

rcon_password = os.getenv('RCON_PASSWORD').strip('{').strip('}')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!gg ", case_insensitive=True, intents=intents)
#bot.timer_manager = timers.TimerManage(bot)

bot_user_role = 'unfunny'
admin_role = 'God'


@bot.event
async def on_ready():
    print('We have logged in as {0.user} and is connected to the following guilds:\n'.format(bot))
    for g in bot.guilds:
        print('{0.name}\n'.format(g))
    
@bot.command(name="silence",help="Silences everybody else in your current voice channel")
@commands.has_role(bot_user_role)
async def silence(ctx, *args):
	print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
	for mem in ctx.message.author.voice.channel.members:
		if mem != ctx.message.author:
			await mem.edit(mute = True)
			print("---" + BF.user2name(mem) + " has been muted")
	return

@bot.command(name="unsilence",help="Unsilences everybody else in your current voice channel")
@commands.has_role(bot_user_role)
async def unsilence(ctx, *args):
	print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
	for mem in ctx.message.author.voice.channel.members:
		await mem.edit(mute = False)
		print("---" + BF.user2name(mem) + " has been unmuted")
	return


@bot.command(name="bath",help="Moves specified users to the bath")
@commands.has_role(bot_user_role)
async def bath(ctx, *args):
    guild = ctx.message.channel.guild
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    vic = []
    if ctx.message.mentions:
        for mem in ctx.message.mentions:
            if (BF.user2name(mem) == "shadowdaf#1337"):
                vic.append(BF.user2name(ctx.message.author))
            else:
                vic.append(BF.user2name(mem))
    else:
        vic.append(BF.find_jim(guild))
    mem, membList = BF.getMembers(guild)
    bath_chan = BF.getVoiceChannels(guild)['Bath']
    print(vic)
    for v in vic:
        victim = guild.get_member(mem[v])
        await victim.move_to(guild.get_channel(bath_chan))
        print("---{0} moved {1} to the bath!".format(BF.user2name(ctx.message.author),v))
    return
        
    
@bot.command(name="gdi",help="prints discord server info to console")
@commands.has_role(admin_role)
async def gdi(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    ctime = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d_%Hh%Mm%Ss")
    file = os.path.join(os.getcwd(),"discord_infos",ctime+".txt")
    print(file)
    with open(file, "w") as f:
        for g in bot.guilds:
            f.write(g.name+":\n")
            membs, membList = BF.getMembers(g)
            roles = BF.getRoles(g)
            vcs = BF.getVoiceChannels(g)
            
            f.write("    Members:\n")
            for mL in membList:
                f.write("        "+str(mL)+"\n")
            f.write("    Roles:\n")
            for r in roles:
                f.write("       "+str(r)+"\n")
            f.write("   Voice channel names:\n")
            for vc in vcs:
                f.write("       "+str(vc)+"\n")

@bot.command(name="whereis", help="Will locate users voice channel")
@commands.has_role(admin_role)
async def whereis(ctx, user, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    name = BF.user2name(ctx.message.mentions[0])
    channel = BF.get_user_vc(ctx.message.guild,name)
    if channel:
        await ctx.send("{0} is currently in the channel {1} in the {2} section".format(name,channel.name,channel.category))
    else:
        await ctx.send("{0} is not currently connected to the server".format(name))
    return


@bot.command(name="schpasta", help="Tells you what voice channel a user is in")
@commands.has_role(bot_user_role)
async def schpasta(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    await ctx.send("MostlySchisty Exploiter He use No Recoil+Trigger(Aimbot)+Esp(WallHack)")
    return

@bot.command(name="unixtime", help="Takes a time and date and gives it in unix time")
@commands.has_role(bot_user_role)
async def unix_time(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    intime = " ".join(ctx.message.content.split(" ")[2:])
    utime = BF.get_unix_time(intime)
    print(utime)
    await ctx.send("Unix time is {0}".format(str(utime)))
    return

@bot.command(name="nickbackup", help="Backs up all nicknames")
@commands.has_role(admin_role)
async def backup_nicknames(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    guild = ctx.message.channel.guild
    await BF.backup_user_nicknames(guild)
    await ctx.send("Backup has been completed")
    return



@bot.command(name="changenick", help="Changes a persons nickname")
@commands.has_role(admin_role)
async def change_nickname(ctx,*args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    users = ctx.message.mentions
    try:
        newnick = ctx.message.content.split()[3]
    except:
        newnick = None
    for u in users:
        try:
            await u.edit(nick=newnick)
        except:
            print("Failed to change name of {0}".format(u))
    return
    
@bot.command(name="nickrestore", help="Resores all nicknames from backup")
@commands.has_role(admin_role)   
async def restore_nicknames(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    guild = ctx.message.channel.guild
    async with aiofiles.open("{0}.csv".format(guild), mode="r", encoding="utf-8",newline="") as afp:
        async for row in aiocsv.AsyncReader(afp):
            member = guild.get_member(int(row[0]))
            old_nick = row[2]
            if old_nick == '':
                old_nick = None
            print(old_nick)
            print(member)
            try:
                await member.edit(nick=old_nick)
            except:
                print("Failed to change name of {0}".format(member))
    return

@bot.command(name="call_you_bruce", help="Bruce")
@commands.is_owner()
async def call_you_bruce(ctx, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    guild = ctx.message.channel.guild
    for m in guild.members:
        try:
            await m.edit(nick="Bruce")
        except:
            print("Failed to change name of {0}".format(m))
    return



@bot.command(name="mcstatus", help = "Gives information on minecraft server at given ip")
@commands.has_role(bot_user_role)
async def minecraft_server_status(ctx, ip, *args):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    ip_address = ctx.message.content.split(" ")[2]
    #print(ip_address)
    out = BF.get_mc_status(ip_address)
    status = out.pop("status")
    mc_thumb = "attachment://"+os.path.join(os.getcwd(),"images","mc.png")
    if status == -1:
        await ctx.send("That is not a valid IP")
    else:
        if out["players"]:
            players = "\n".join(out["players"])
            desc = "{0} \n>>> {1}".format(out["description"],players)
        else:
            desc = out["description"]
        embed = discord.Embed(colour=out["colour"],title=out["title"],description=desc)
        embed.set_thumbnail(url=mc_thumb)
        embed.set_footer(text="Last updated {0}".format(BF.get_current_time()))
        """
        if out["players"]:
            content = "\n".join(out["players"])
            embed.add_field(title="hello",value="awesome",inline=False)
        """
        
        msg = await ctx.send(embed=embed)
        while (status != -1):
            await asyncio.sleep(60)
            out = BF.get_mc_status(ip_address)
            if out["players"]:
                players = "\n".join(out["players"])
                desc = "{0} \n>>> {1}".format(out["description"],players)
            else:
                desc = out["description"]
            embed = discord.Embed(colour=out["colour"],title=out["title"],description=desc)
            embed.set_thumbnail(url=mc_thumb)
            embed.set_footer(text="Last updated {0}".format(BF.get_current_time()))
            await msg.edit(embed = embed)
    return
"""
@bot.command(name="reminder", help="Sets a reminder - format is !gg reminder YYYY-MM-DD_hh:mm title")
@commands.has_role(bot_user_role)
async def reminder(ctx, date, text):
    print(datetime.datetime.strftime(datetime.datetime.now(),"[%Y-%m-%d_%H:%M:%S]") +" {0} executed command {1}".format(BF.user2name(ctx.message.author),ctx.message.content))
    date = datetime.datetime.strptime(date, "%Y-%m-%d_%H:%M")
    bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, ctx.author.id, text)).start()
    return

@bot.command(name="timer", help="Sets a timer - format !gg timer H:M:S")
@commands.has_role(bot_user_role)
async def my_timer(ctx, date, text):
    dl = date.split(":")
    try:
        dl = list(map(float,dl))
    except:
        await ctx.send("You didn't use the correct timer format")
        return
    if len(dl) == 3:
        tdelta = datetime.timedelta(hours=dl[0],minutes=dl[1],seconds=dl[2])
        date = datetime.datetime.now()+tdelta
        bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, ctx.author.id, text)).start()
        print("starting timer")
    else:
        await ctx.send("You didn't use the correct timer format")
    return

@bot.event
async def on_reminder(channel_id, author_id, text):
    channel = bot.get_channel(channel_id)
    await channel.send("<@{0}>, reminder for {1}".format(author_id, text))
"""

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        pic = os.path.join(os.getcwd(),"images","blockjim.png")
        await ctx.send(file=discord.File(pic))
        await ctx.send("Jimbob has blocked your path, he says you do not have permission to use that command")
		
if __name__ == "__main__":
	print("bot is now running")
	bot.run(TOKEN)

"""
///TO DO LIST
make timers

"""
