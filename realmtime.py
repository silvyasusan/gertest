import os
import discord
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.environ.get("TOKEN") 
CHANNEL_ID =1378306927620264056

REAL_WORLD_START = datetime(2024, 9, 12, 6, 0, 0)
IN_GAME_START = datetime(1450, 9, 12, 6, 0, 0)

WEEKDAYS = ["Sunfire", "Moonday", "Earthday", "Windday", "Stoneday", "Darkday"]
MONTHS = [
    "Embermoon", "Frostwane", "Stormtide", "Bloomshade",
    "Greengale", "Highsun", "Duskwither", "Ashfall",
    "Dawnrise", "Starveil", "Hollowshade", "Snowmourn"
]

class TimeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        # Don't create task here!

    async def setup_hook(self):
        # Called once before the bot connects
        self.bg_task = self.loop.create_task(self.update_time_loop())

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def update_time_loop(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Error: Channel ID {CHANNEL_ID} not found.")
            return

        pinned = await channel.pins()
        if pinned:
            message = pinned[0]
        else:
            message = await channel.send("Initializing in-game time...")
            await message.pin()

        while not self.is_closed():
            now = datetime.utcnow()
            elapsed_real = now - REAL_WORLD_START
            in_game_seconds = elapsed_real.total_seconds() * 2
            current_game_time = IN_GAME_START + timedelta(seconds=in_game_seconds)

            hour = current_game_time.hour
            minute = current_game_time.minute
            icon = "🌞" if 6 <= hour < 18 else "🌙"
            time_str = f"{hour:02d}:{minute:02d}"

            day_of_week = WEEKDAYS[current_game_time.toordinal() % len(WEEKDAYS)]
            month_index = (current_game_time.month - 1) % len(MONTHS)
            month = MONTHS[month_index]
            day = current_game_time.day
            year = current_game_time.year

            embed = discord.Embed(
                title=f"{icon} Time of the Realm",
                color=0x00FFCC
            )
            embed.add_field(name="📅 Date", value=f"**{day_of_week}, {day} {month}, Year {year}**", inline=False)
            embed.add_field(name="⏳ Hour", value=f"**{time_str}**", inline=True)
            embed.set_footer(text="Time flows swiftly in this world...")

            await message.edit(content=None, embed=embed)
            await asyncio.sleep(30)

client = TimeBot()
client.run(TOKEN)
