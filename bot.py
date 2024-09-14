import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("TOKEN")
words = [
    "student", "regional", "distinct", "hypothesis", "pseudo code",
    "psychology", "scissors", "percentage", "terrorism", "national", "average",
    "avengers", "horizontal", "vertical", "diagonal", "global", "supernova",
    "apple", "table", "cricket", "football", "tennis", "hockey",
    "table tennis", "chess", "void", "movie", "story", "animal",
    "human being", "elephant", "tiger", "crocodile", "horse", "buffalo",
    "donkey", "monkey", "random", "combine", "permutation", "examine",
    "determine", "alien", "time travel", "black hole", "worm hole",
    "interstellar", "adventure", "disaster","trigger", "nigger", "digger"
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='',intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command(name='guesswhatbot')
async def start_hangman(ctx):
    secret_word = random.choice(words)
    display_word = ['^' if letter != ' ' else ' ' for letter in secret_word]

    await ctx.send(f"Hello {ctx.author.name}! You will get 10 chances to guess the correct word.")
    await ctx.send("Enter any letter to find if it is present in the word.")
    await ctx.send("If you think you know the word, enter 'ans <your_guess>'.")
    

    guess_count = 0

    while guess_count < 10:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        guess = await bot.wait_for('message', check=check)
        guess = guess.content.lower().strip()
        guess_count += 1
       
        if guess.startswith('ans '):
            if guess[4:] == secret_word:
                await ctx.send("Finally u solved it nigga")
                break
            else:
                await ctx.send("You are an imbecile, Nigga")
                continue

        await ctx.send(f"Nigga you have {10 - guess_count} attempts left")

        if len(guess) != 1 or not guess.isalpha():
            await ctx.send("Enter a valid letter or 'ans <your_guess>'.")
            guess_count -= 1
            continue

        for i, letter in enumerate(secret_word):
            if letter == guess:
                display_word[i] = guess

        await ctx.send(" ".join(display_word))

        if ''.join(display_word) == secret_word:
            await ctx.send("Finally u solved it nigga")
            break

    else:
        await ctx.send(f"You LOST just like your crush's virginity! The word was: {secret_word}")

bot.run(TOKEN)
