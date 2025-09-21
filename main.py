import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.config.settings import BOT_TOKEN
from app.bot.handlers import start, stats

load_dotenv()


async def set_bot_commands(bot: Bot):
    commands = [
    BotCommand(command='start', description="Start"),
    BotCommand(command='stats', description="View campaign statistics")
    ]


    await bot.set_my_commands(commands)


async def main():
    print('Starting PostAd Dashboard Bot...')
    print("Using Google Sheets for data")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await set_bot_commands(bot)

    dp.include_router(stats.router)
    dp.include_router(start.router)

    print("Bot started.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




