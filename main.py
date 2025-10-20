from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

bot = Bot(token="7886069810:AAFgcFNP_1PbM4cfKIkIZnniMnBWHvOEoEc")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

