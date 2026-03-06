import asyncio, logging
from aiogram import F, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from credentials import bot_token

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Это была команда старт')

@dp.message(F.text == "!айди")
async def get_chat_id(message: Message):
    await message.answer(f"Айди этого чата => {message.chat.id}")

async def main():
    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')]
                        )
    await dp.start_polling(bot)

asyncio.run(main())