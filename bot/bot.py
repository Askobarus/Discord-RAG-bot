import discord
from discord.ext import commands
from repository import save_messages 
from schemas.messages import SMessage

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
        await ctx.send("Собираю сообщения из канала...")
        
        messages_data = []
        async for message in ctx.channel.history(limit=limit):
            msg = SMessage.from_discord_message(message, ctx.channel.id)
            if msg:  # Пропускаем пустые сообщения
                messages_data.append(msg.model_dump())
        
        if not messages_data:
            await ctx.send("Сообщений для сохранения не найдено.")
            return

        await ctx.send("Сохраняю в базу данных...")
        try:
            saved_count = await save_messages(messages_data)
            await ctx.send(f"Успешно сохранено/обновлено **{saved_count}** сообщений.")
        except Exception as e:
            await ctx.send(f"Произошла ошибка при записи в БД. Проверьте логи.")
            print(f"DB Error: {e}")

    return bot