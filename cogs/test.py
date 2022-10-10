import discord
from discord.ext import commands

class Base(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("BOT IS ONLINE") 
    @commands.Cog.listener()
    async def on_message(self, message):
        bot =commands.Bot(command_prefix="+",intents=discord.Intents.all())
        if message.author == bot.user:
            return
        if message.content.upper()=="HELLO":
            await message.channel.send('Hello!')
        await bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(member):
        channel = member.guild.system_channel
        await channel.send(f'Welcome {member.mention} to the server!')


    @commands.Cog.listener()
    async def on_member_remove(member):
        channel = member.guild.system_channel
        await channel.send(f"{member.mention} Goodbye,Loser")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    await bot.add_cog(Base(bot))