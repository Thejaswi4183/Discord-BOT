import os
import random
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Slash command: /ping
@bot.slash_command(name="ping", description="Check bot latency")
async def ping(ctx: discord.ApplicationContext):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Pong! Latency: {latency}ms")

# Slash command: /hello
@bot.slash_command(name="hello", description="Say hello")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello, {ctx.author.name}!")

# Slash command: /roll
@bot.slash_command(name="roll", description="Roll a dice between 1 and 6")
async def roll(ctx: discord.ApplicationContext):
    result = random.randint(1, 6)
    await ctx.respond(f"{ctx.author.name} rolled a {result}!")

# Slash command: /clear  
@bot.slash_command(name="clear", description="Delete a number of messages from this channel")
async def clear(ctx: discord.ApplicationContext, amount: int):
    if amount < 1 or amount > 100:
        await ctx.respond("Please provide a number between 1 and 100.", ephemeral=True)
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.respond(f"Deleted {len(deleted)} messages.", ephemeral=True)

# Slash command: /userinfo
@bot.slash_command(name="userinfo", description="Get info about a user")
async def userinfo(ctx: discord.ApplicationContext, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.respond(embed=embed)

# Slash command: /serverinfo
@bot.slash_command(name="serverinfo", description="Get info about this server")
async def serverinfo(ctx: discord.ApplicationContext):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
    embed.add_field(name="ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=str(guild.owner), inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
    await ctx.respond(embed=embed)

# Slash command: /avatar
@bot.slash_command(name="avatar", description="Get the avatar of a user")
async def avatar(ctx: discord.ApplicationContext, member: discord.Member = None):
    member = member or ctx.author
    await ctx.respond(member.avatar.url if member.avatar else member.default_avatar.url)

# Slash command: /say
@bot.slash_command(name="say", description="Make the bot say something")
async def say(ctx: discord.ApplicationContext, message: str):
       
    await ctx.channel.send(message)
    await ctx.respond("Message sent", ephemeral=True)

# Slash command: /remindme
@bot.slash_command(name="remindme", description="Set a reminder in seconds")
async def remindme(ctx: discord.ApplicationContext, seconds: int, *, reminder: str):
    await ctx.respond(f"Okay, I will remind you in {seconds} seconds!", ephemeral=True)
    await asyncio.sleep(seconds)
    await ctx.followup.send(f"⏰ Reminder: {reminder}", ephemeral=True)

# Slash command: /flip
@bot.slash_command(name="flip", description="Flip a coin")
async def flip(ctx: discord.ApplicationContext):
    coin = random.choice(["Heads", "Tails"])
    await ctx.respond(f"Coin flip: {coin}")
    
# Slash command: /reverse  
@bot.slash_command(name="reverse", description="Reverse any text you enter")
async def reverse(ctx: discord.ApplicationContext, *, message: str):
    reversed_text = message[::-1]
    await ctx.respond(f"🔁 {reversed_text}")

bot.run(TOKEN)
