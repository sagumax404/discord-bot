import asyncio
import discord
from discord.ext import commands
import os
bot = commands.Bot(command_prefix = "+",intents=discord.Intents.all())

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start("token")

asyncio.run(main())