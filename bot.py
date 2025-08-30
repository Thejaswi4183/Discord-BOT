import os
import random
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

bot.run(TOKEN)
