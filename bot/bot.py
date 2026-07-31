import discord
from discord.ext import commands
import logging


def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"My name is {bot.user.name}")

    @bot.event
    async def on_member_join(member):
        await member.send(f"HI {member.name}!")

    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @bot.command()
    async def check(ctx):
        pass

    return bot