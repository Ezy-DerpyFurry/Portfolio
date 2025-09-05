### Imports ###

import discord                      # Base discord imports
from discord.ext import commands
from discord import app_commands

from mcstatus import JavaServer     # Minecraft imports

import subprocess                   # Extras
import math 
import asyncio
import threading
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

server_ip = "server ip here"                                # For Example hypixel.net or example.minehut.gg
url = "url to your world in dynamap"                        # For Example (https://ip/up/world/{your world here now}/0) MUST HAVE DYNAMAP WITH LIKE ALL SETTINGS ENABLED
prefix = "$"                                                # Put None if you don't want prefix commands

VERSION = "1.21/1.21.1"                                     # Your server version here
TOKEN = "bot token here"                                    # Your bot token goes here.
ALLOWED_CHANNEL_ID = 1                                      # Channel you want the commands to go to and be restricted to
BOT_OWNER_ID,USER = 719313462324625488, "Ezy 2.0 alters"    # This is my discord stuff for credits to the bot I'd prefer if you didn't replace it please :3
PATH_TO_MESSAGE_FOLDER = "path to message folder"           # This is for if you record messages/save them to a file.txt Don't touch if you don't wanna use it

### VARIABLES HERE

server = JavaServer.lookup("server ip here")  
bot = commands.Bot(command_prefix="$", intents=intents)
intents = discord.Intents.default()
intents.message_content = True

### Functions for the bot later on ###

def in_main_channel():
    async def predicate(ctx):
        allowed_channel_id = ALLOWED_CHANNEL_ID
        if ctx.channel.id != allowed_channel_id:
            return False
        return True
    return commands.check(predicate)

if PATH_TO_MESSAGE_FOLDER != "path to message folder":
    def chat_monitor():
        last_timestamp = 0

        while True:
            try:
                r = requests.get(f"{url}{last_timestamp}")
                data = r.json()

                last_timestamp = data.get("timestamp", last_timestamp)

                for update in data.get("updates", []):
                    if update.get("type") == "chat":
                        player = update["playerName"]
                        msg = update["message"]
                        with open(PATH_TO_MESSAGE_FOLDER, "a") as file:
                            now = datetime.now(ZoneInfo("America/New_York"))
                            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                            file.write(f"{player}: {msg} | Timestamp: {timestamp}\n")

            except Exception as e:
                print("Error:", e)

            time.sleep(0.1)

    threading.Thread(target=chat_monitor, daemon=False).start()

def is_main_channel_B():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.channel.id == ALLOWED_CHANNEL_ID
    return app_commands.check(predicate)

def is_owner_or_admin():
    async def predicate(ctx):
        OWNER_ID = BOT_OWNER_ID

        if ctx.author.id == OWNER_ID:
            return True

        if ctx.author.guild_permissions.administrator:
            return True

        return False
    return commands.check(predicate)

def if_dynamap():
    if url != "url to your world in dynamap":
        return True
    return False

def get_player_online():
    r = requests.get(url)
    data = r.json()

    players = data.get("players", [])
    playerinfo = []
    for player in players:
        info = {
            "name": player.get("name"),
            "armor": player.get("armor"),
            "health": player.get("health"),
            "world": player.get("world"),
            "x": player.get("x"),
            "y": player.get("y"),
            "z": player.get("z")
        }
        playerinfo.append(info)
    return playerinfo

### Slash Commands ###

@bot.event
async def on_ready():
    print(f"{bot.user} is now online and active.")
    global channel_id
    channel_id = bot.get_channel(ALLOWED_CHANNEL_ID)
    await bot.tree.sync()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(f"You can only use commands in <#{ALLOWED_CHANNEL_ID}>.", ephemeral=True)

@bot.tree.command(name="playerinfo", description="See a online players info.")
@if_dynamap()
@is_main_channel_B()
async def playerinfo(interaction: discord.Interaction, name: str):
    players = get_player_online()
    for a in players:
        rank, p_name = a['name'].split(" ")
        if p_name.lower() == name.lower():
            embed = discord.Embed(
                title=f"{p_name}'s stats",
                description=f"get {p_name}'s health, armor, and current world.",
                color=discord.Color.red()
            )

            embed.add_field(name=f"Rank: {rank}", value=f"Armor amount: {a['armor']}\nHealth: {a['health']}\nWorld: {a['world']}", inline=True)

            botowner = await bot.fetch_user(BOT_OWNER_ID)
            embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            embed.set_thumbnail(url=bot.user.avatar.url)

            await interaction.response.send_message(embed=embed)

            if interaction.user.guild_permissions.administrator:
                await interaction.followup.send(f"Their coords are: X={a['x']} Y={a['y']} Z={a['z']} (You see this cause you're an administrator.)", ephemeral=True)

@bot.tree.command(name="weather", description="Checks the server's weather")
@if_dynamap()
@is_main_channel_B()
async def weather(interaction: discord.Interaction):
    r = requests.get(url)
    data = r.json()

    try:
        is_storming = data.get("hasStorm")
        is_thundering = data.get("isThundering")
        server_time = data.get("servertime")
        hours = (server_time / 1000 + 6) % 24
        minutes = (server_time % 1000) * 60 / 1000
    except:
        print("Unkown values")

    embed = discord.Embed(
        title="Weather",
        description="The servers weather",
        color=discord.Color.blue()
    )
    embed.add_field(name="Current:", value=f" Raining: {is_storming}\n Thunder: {is_thundering}\n Time (In ticks): {server_time}\n Time: {int(hours):02d}:{int(minutes):02d}", inline=True)
    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="watchchat", description="Enables minecraft chat messages here")
@if_dynamap()
@is_main_channel_B()
@is_owner_or_admin()
async def watchchat(interaction: discord.Interaction, state: bool):
    global watching
    watching = state

    r = requests.get(f"{url}0")
    data = r.json()
    last_timestamp = data.get("timestamp", 0)

    def chatb_monitor():
        nonlocal last_timestamp

        while watching:
            try:
                r = requests.get(f"{url}{last_timestamp}")
                data = r.json()

                for update in data.get("updates", []):
                    ts = update.get("timestamp", 0)

                    if ts <= last_timestamp:
                        continue

                    if update.get("type") == "chat":
                        player = update["playerName"]
                        msg = update["message"]
                        asyncio.run_coroutine_threadsafe(channel_id.send(f"[MC] | {player}: {msg}"), bot.loop)

                    if ts > last_timestamp:
                        last_timestamp = ts

            except Exception as e:
                print("Error:", e)

            time.sleep(0.1)

    if watching:
        threading.Thread(target=chatb_monitor, daemon=True).start()
        await interaction.response.send_message("Player messages will now be sent here.")
    else:
        await interaction.response.send_message("Player messages will no longer be sent here.")

@bot.tree.command(name="online", description="Check if the server is online")
@is_main_channel_B()
async def online(interaction: discord.Interaction):
    status = server.status()
    if status:
        print(interaction.user.mention)
        await interaction.response.send_message("Server is online.")
    else:
        print(interaction.user.mention)
        await interaction.response.send_message("Server is offline.")

@bot.tree.command(name="notify", description="Enabled/Disables join/leave messages from the discord bot")
@is_main_channel_B()
@is_owner_or_admin()
async def notify(interaction: discord.Interaction, state: bool):
    global Notify
    Notify = state
    status = server.status()
    if status.players.sample:
        prev_players = [p.name for p in status.players.sample]
    else:
        prev_players = []

    def monitor():
        nonlocal prev_players
        while Notify:
            try:
                status = server.status()
                if status.players.sample:
                    current_players = [p.name for p in status.players.sample]
                else:
                    current_players = []

                added = [p for p in current_players if p not in prev_players]
                removed = [p for p in prev_players if p not in current_players]

                for player in added:
                    asyncio.run_coroutine_threadsafe(channel_id.send(f"{player} has joined the server."), bot.loop)
                for player in removed:
                    asyncio.run_coroutine_threadsafe(channel_id.send(f"{player} has left the server."), bot.loop)

                prev_players = current_players

            except Exception as e:
                print(f"Server offline or error: {e}")

            time.sleep(0.5)
    if Notify:
        threading.Thread(target=monitor, daemon=True).start()
        await interaction.response.send_message("Player joins and leaves will now be monitored in this chat.")
    else:
        await interaction.response.send_message("Player joins and leaves will no longer be monitored in this chat.")

@bot.tree.command(name="ping", description="Check MC server's ping/latency")
@is_main_channel_B()
async def pingserver(interaction: discord.Interaction):
    status = server.status()
    latency = math.floor(status.latency)
    await interaction.response.send_message(f"The server latency is {latency}ms")

@bot.tree.command(name="players", description="See all the players online")
@is_main_channel_B()
async def playercount(interaction: discord.Interaction):
    status = server.status()

    embed = discord.Embed(
        title="Players online",
        description=f"Here’s the current online players.\n{status.players.online}/{status.players.max}",
        color=discord.Color.green()
    )

    if status.players.sample:
        names = [p.name for p in status.players.sample]
        player_list = "\n".join(f"- {n}" for n in names)
    else:
        player_list = "No players in server."

    try:
        embed.add_field(name="Players: ", value=player_list, inline=True) 
    except Exception as e:
        print("no players or error | ERROR: ", e)
        embed.add_field(name="Players: ", value="No players online", inline=True)

    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="Check MC server's info")
@is_main_channel_B()
async def serverinfo(interaction: discord.Interaction):
    status = server.status()
    embed = discord.Embed(
        title="AncientEarthSMP Server Info 🌍",
        description="Here’s the current status of the server!",
        color=discord.Color.blue()
    )

    latency = math.floor(status.latency)

    if status:
        a = "Server is online."
    else:
        a = "Server is offline."

    embed.add_field(name="Status", value=a, inline=True)
    embed.add_field(name="Players", value=f"{status.players.online} / {status.players.max}", inline=True)
    embed.add_field(name="Latency", value=f"{latency} ms", inline=True)
    embed.add_field(name="IP: ", value="AncientEarthSMP.mcserv.fun", inline=False)
    embed.add_field(name="Version", value="{VERSION}", inline=True)

    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await interaction.response.send_message(embed=embed)

### PREFIXED COMMANDS ###

@bot.command()
@if_dynamap()
@in_main_channel()
async def weather(ctx):
    r = requests.get(url)
    data = r.json()

    try:
        is_storming = data.get("hasStorm")
        is_thundering = data.get("isThundering")
        server_time = data.get("servertime")
        hours = (server_time / 1000 + 6) % 24
        minutes = (server_time % 1000) * 60 / 1000
    except:
        print("Unkown values")

    embed = discord.Embed(
        title="Weather",
        description="The servers weather",
        color=discord.Color.blue()
    )
    embed.add_field(name="Current:", value=f" Raining: {is_storming}\n Thunder: {is_thundering}\n Time (In ticks): {server_time}\n Time: {int(hours):02d}:{int(minutes):02d}", inline=True)
    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await channel_id.send(embed=embed)

@bot.command(aliases=['isonline', 'is_online'])
@in_main_channel()
async def online(ctx):
    status = server.status()
    if status:
        await channel_id.send("Server is online.")
    else:
        await channel_id.send("Server is offline.")

@bot.command()
@in_main_channel()
@is_owner_or_admin()
async def notify(ctx, state: bool):
    global Notify
    Notify = state
    status = server.status()
    if status.players.sample:
        prev_players = [p.name for p in status.players.sample]
    else:
        prev_players = []

    def monitor():
        nonlocal prev_players
        while Notify:
            try:
                status = server.status()
                if status.players.sample:
                    current_players = [p.name for p in status.players.sample]
                else:
                    current_players = []

                added = [p for p in current_players if p not in prev_players]
                removed = [p for p in prev_players if p not in current_players]

                for player in added:
                    asyncio.run_coroutine_threadsafe(channel_id.send(f"{player} has joined the server."), bot.loop)
                for player in removed:
                    asyncio.run_coroutine_threadsafe(channel_id.send(f"{player} has left the server."), bot.loop)

                prev_players = current_players

            except Exception as e:
                asyncio.run_coroutine_threadsafe(channel_id.send(f"Server offline or error: {e}"), bot.loop)

            time.sleep(0.5)
    if Notify:
        threading.Thread(target=monitor, daemon=True).start()
        await channel_id.send("Player joins and leaves will now be monitored in this chat.")
    else:
        await channel_id.send("Player joins and leaves will no longer be monitored in this chat.")

@bot.command(aliases=['pinfo','p_info'])
@if_dynamap()
@in_main_channel()
async def playerinfo(ctx, name: str):
    players = get_player_online()
    for a in players:
        rank, p_name = a['name'].split(" ")
        if p_name.lower() == name.lower():
            embed = discord.Embed(
                title=f"{p_name}'s stats",
                description=f"get {p_name}'s health, armor, and current world.",
                color=discord.Color.red()
            )

            embed.add_field(name=f"Rank: {rank}", value=f"Armor amount: {a['armor']}\nHealth: {a['health']}\nWorld: {a['world']}", inline=True)

            botowner = await bot.fetch_user(BOT_OWNER_ID)
            embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            embed.set_thumbnail(url=bot.user.avatar.url)

            await channel_id.send(embed=embed)

@bot.command(aliases=['ping_server', 'ping'])
@in_main_channel()
async def pingserver(ctx):
    status = server.status()
    latency = math.floor(status.latency)
    await channel_id.send(f"The server latency is {latency}ms")

@bot.command(aliases=['player_count','players'])
@in_main_channel()
async def playercount(ctx):
    status = server.status()

    embed = discord.Embed(
        title="Players online",
        description=f"Here’s the current online players.\n{status.players.online}/{status.players.max}",
        color=discord.Color.green()
    )

    if status.players.sample:
        names = [p.name for p in status.players.sample]
        player_list = "\n".join(f"- {n}" for n in names)
    else:
        player_list = "No players in server."

    try:
        embed.add_field(name="Players: ", value=player_list, inline=True) 
    except Exception as e:
        print("no players or error | ERROR: ", e)
        embed.add_field(name="Players: ", value="No players online", inline=True)

    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await channel_id.send(embed=embed)

@bot.command(aliases=['watch_chat'])
@if_dynamap()
@is_main_channel_B()
@is_owner_or_admin()
async def watchchat(ctx, state: bool):
    global watching
    watching = state

    r = requests.get(f"{url}0")
    data = r.json()
    last_timestamp = data.get("timestamp", 0)

    def chatb_monitor():
        nonlocal last_timestamp

        while watching:
            try:
                r = requests.get(f"{url}{last_timestamp}")
                data = r.json()

                for update in data.get("updates", []):
                    ts = update.get("timestamp", 0)

                    if ts <= last_timestamp:
                        continue

                    if update.get("type") == "chat":
                        player = update["playerName"]
                        msg = update["message"]
                        asyncio.run_coroutine_threadsafe(channel_id.send(f"[MC] | {player}: {msg}"), bot.loop)

                    if ts > last_timestamp:
                        last_timestamp = ts

            except Exception as e:
                print("Error:", e)

            time.sleep(0.1)

    if watching:
        threading.Thread(target=chatb_monitor, daemon=True).start()
        await channel_id.send("Player messages will now be sent here.")
    else:
        await channel_id.send("Player messages will no longer be sent here.")

@bot.command(aliases=['info','server_info', 'ip'])
@in_main_channel()
async def serverinfo(ctx):
    status = server.status()
    embed = discord.Embed(
        title="AncientEarthSMP Server Info 🌍",
        description="Here’s the current status of the server!",
        color=discord.Color.blue()
    )

    latency = math.floor(status.latency)

    if status:
        a = "Server is online."
    else:
        a = "Server is offline."

    embed.add_field(name="Status", value=a, inline=True)
    embed.add_field(name="Players", value=f"{status.players.online} / {status.players.max}", inline=True)
    embed.add_field(name="Latency", value=f"{latency} ms", inline=True)
    embed.add_field(name="IP: ", value="AncientEarthSMP.mcserv.fun", inline=False)
    embed.add_field(name="Version", value="{VERSION}", inline=True)

    botowner = await bot.fetch_user(BOT_OWNER_ID)
    embed.set_footer(text=f"Bot by {USER}", icon_url=botowner.avatar.url)
    embed.timestamp = discord.utils.utcnow()

    embed.set_thumbnail(url=bot.user.avatar.url)

    await channel_id.send(embed=embed)

### token stuffz 3: ###

"""
TOKEN = None

with open("URL TO TOKEN HERE", "r") as file:
    for current_line, content in enumerate(file, start=1):
        if current_line == 1:
            TOKEN = content.strip()
            break
"""

bot.run(TOKEN)
