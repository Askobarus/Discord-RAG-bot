import discord
from discord.ext import commands
import logging, json


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
        await member.send(f"HI, {member.name}!")

    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")
    
    @bot.command()
    async def poka(ctx):
        await ctx.send(f"Проваливай, {ctx.author.mention}!")

    @bot.command()
    async def check(ctx, limit: int = 100):
        """Сохраняет историю канала в файл"""
        await ctx.send("Начинаю выгрузку...")
        
        messages = []
        async for message in ctx.channel.history(limit=limit):
            messages.append({
                "id": message.id,
                "author": message.author.name,
                "content": message.content,
                "timestamp": str(message.created_at)
            })
        
        filename = f"channel_{ctx.channel.id}_messages.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        await ctx.send(f"Сохранено {len(messages)} сообщений в {filename}")

    return bot