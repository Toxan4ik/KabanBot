import asyncio
import random
import re
import urllib.request
from datetime import timedelta
import datetime
import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token="7746997930:AAHG7ADvjzTKjv5eTRb-oiwhov-pA5vWEYQ")
dp = Dispatcher()

@dp.message(Command("info"))
async def info_command(message: types.Message):
    await message.reply(
        "Вот все команды, по которым вы можете обращаться ко мне:\n\n"
        "/criminal --- Узнать свою статью УК РФ\n"
        "/dice --- Бросить кубик\n"
        "/bouling --- Боулинг\n"
        "/target --- Попасть в мишень\n"
        "/casino --- Играть в казино\n"
        "/report [@провинившийся] [причина] --- Кинуть жб\n"
        "/info --- Информация о командах")

@dp.message(Command("dice"))
async def dice_command(message: types.Message):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    dice_message = await bot.send_dice(message.chat.id, emoji="🎲")
    await dice_message.reply(f"{message.from_user.first_name}, вам выпало число: {dice_message.dice.value}")

@dp.message(Command("target"))
async def target_command(message: types.Message):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    target_messages = await bot.send_dice(message.chat.id, emoji="🎯")
    await target_messages.reply(f"{message.from_user.first_name}, вы попали в число: {target_messages.dice.value}")

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    casino_message = await bot.send_dice(message.chat.id, emoji="🎰")
    await casino_message.reply(f"Ваш выигрыш {message.from_user.first_name}: {casino_message.dice.value}")

@dp.message(Command("bouling"))
async def bouling_command(message: types.Message):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    bouling_message = await bot.send_dice(message.chat.id, emoji="🎳")
    await bouling_message.reply(f"Ваш выигрыш {message.from_user.first_name}: {bouling_message.dice.value}")

@dp.message(Command("criminal"))
async def criminal_command(message: types.Message):
    while True:
        url = "https://rulaws.ru/uk/?ysclid=mh0o16yda4718036120"
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        vibor = random.randint(143, len(soup.find("table").find_all("tr")))
        if "Глава" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "Раздел" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "ЧАСТЬ ОБЩАЯ" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","")  and "Утратила силу" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n",""):
            await message.reply("👤 "+str(message.from_user.username)+" обвиняется по "+str(soup.find("table").find_all("tr")[vibor].text).replace("\n","").replace("Статья","статье ⚖️")+" 🔗")
            break

@dp.message(Command("report"))
async def report_com(message: types.Message):
    text = str(message.text).replace("/report ", "").replace("/report", "")
    if str(text).replace(" ", "") != "":
        Name = str(text).split()[0]
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
            
        NameAndLastname = ""
        if message.from_user.first_name is not None:
            NameAndLastname += str(message.from_user.first_name) + " "
        if message.from_user.last_name is not None:
            NameAndLastname += str(message.from_user.last_name) + " "
        NameAndLastname += f"({message.from_user.username})"
        
        text = text.replace(f"{Name} ", "")
        report_text = f"🛑 РЕПОРТ! 🛑\n\nПользователь: {NameAndLastname} c ID: {message.from_user.id}\nПожаловался на пользователя {Name}\n\nПричина: {text}"
        
        try:
            try:
                await bot.send_message(1828269322, text=report_text)
            except Exception:
                pass
            await bot.send_message(2021260772, text=report_text)
        except Exception:
            await message.answer("🛑 Невозможно отправить репорт, т.к. у админа нет активного чата с ботом 🛑")
    else:
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        await message.answer("🛑 Вы не можете отправить пустую жалобу! 🛑")

async def ban(message, bantime):
    await message.reply(f"Бан на {bantime} мин!")
    now = datetime.datetime.now()
    ban_until = now + timedelta(minutes=bantime)
    timestamp = int(ban_until.timestamp())
    try:
        await bot.restrict_chat_member(chat_id=message.chat.id,user_id=message.from_user.id,permissions=types.ChatPermissions(),until_date=timestamp)
    except Exception:
        pass
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(main())
    except RuntimeError:
        asyncio.run(main())
