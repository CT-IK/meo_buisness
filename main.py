import asyncio, logging
from aiogram import F, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from credentials import bot_token

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')]
                    )

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Это была команда старт')

    # Здесь мы создаем инлайн клавиатуру и создаем ей кнопки с конкретными callback_data
    # (Конкретные данные обрабатываются конкретными хэндлерами)

    # builder = InlineKeyboardBuilder()
    # builder.button(text="хуй", callback_data="btn")


# Вот эту хуйню используйте, как референс

# @dp.callback_query(F.data == "btn")
# async def callback(callback: CallbackQuery):
#     callback_data = str(callback.data)
#     await callback.message.answer("Сосите хуй")


f'''
Мы с Юрием решили, что писюн вы сос\те в этом файлн😘💜
'''

async def main():
    await  bot.delete_
    await dp.start_polling(bot)

asyncio.run(main())