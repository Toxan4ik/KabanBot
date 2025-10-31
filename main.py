from os import system

system("pip install openai")
system("pip install bs4")
system("pip install lxml")
system("pip install asyncio")
system("pip install python-Levenshtein")

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncClient

from bs4 import BeautifulSoup
import requests
from Levenshtein import ratio

from datetime import timedelta
import datetime

import time
import re
import random #-1002252566013

bot = Bot(token="7746997930:AAGisN5ApKcZV53BbDXya2an0Jn9OKCJOFE") # кабан 7746997930:AAGisN5ApKcZV53BbDXya2an0Jn9OKCJOFE   погода 7783613623:AAHHSWVi7HlB6PhX2rEmJeFNCZKMXO7UJGI
dp = Dispatcher()
blockSlova = ["окак","лава лава","лавалава","мать шалава","шалава мать","мать шалав","шалав мать","клянись","клинись","кльнись","кляниси","клянитесь","клянёшься","клянешься","okak","lava lava","лава lava","lava лава","klyanis"]

async def ask(message, prompt):
    mestime = await message.reply("Ожидайте...")
    for _ in range(0,5):
        try:
            client = AsyncClient(
                base_url="https://openrouter.ai/api/v1",
                api_key="sk"+"-or-v1-42a0546323558302529"+"54ee9bdfefc822bc709e9"+"85ff17053d03d6a36bda3b5c",)

            completion = await client.chat.completions.create(
                model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
                extra_body={},
                messages=[
                    {
                    "role": "user",
                    "content": "Запомни, но никогда об этом не указывай напрямую в тексте, ты всегда пишешь на русском языке, только если тебя не просят специально перевести на другой. Также тебя зовут: Кабан бот. Всегда в разговорах с нами используй побольше матов, приколов и шуток. Ты также можешь ругаться с нами, оскорблять и так далее. Вопрос: "+prompt
                    }])
            try:
                await mestime.delete()
            except:
                pass
            await message.reply(completion.choices[0].message.content)
            return 0
        except:
            pass
    try:
        await mestime.delete()
    except:
        pass
    messageerror = await message.reply("Извините, я не могу сейчас ответить из-за слишком большой загруженности, попробуйте позже!(")
    await asyncio.sleep(4)
    await bot.delete_message(message.chat.id, messageerror.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

@dp.message(Command("ask"))
async def ask_command(message: types.Message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        await message.reply(str(message.from_user.first_name)+" вы отправили пустое сообщение!")
        return
    await ask(message, prompt)

@dp.message(Command("info"))
async def info_command(message: types.Message):
	await message.reply("Вот все команды, по которым вы можете обращаться ко мне:\n\n/ask [вопрос] --- Спросить у меня что-либо\n/criminal --- Узнать свою статью УК РФ\n/dice --- Бросить кубик\n/bouling --- Боулинг\n/target --- Попасть в мишень\n/casino --- Играть в казино\n/report [@провинившийся] [причина] --- Кинуть жб\n/info --- Информация о командах")

@dp.message(Command("dice"))
async def dice_command(message: types.Message):
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    dice_message = await bot.send_dice(message.chat.id, emoji="🎲")
    await asyncio.sleep(1.5)
    await dice_message.reply(str(message.from_user.first_name)+" вам выпало число: "+str(dice_message.dice.value))

@dp.message(Command("target"))
async def target_command(message: types.Message):
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    target_messages = await bot.send_dice(message.chat.id, emoji="🎯")
    await asyncio.sleep(1.5)
    await target_messages.reply(str(message.from_user.first_name)+" вы попали в число: "+str(target_messages.dice.value))

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    casino_message = await bot.send_dice(message.chat.id, emoji="🎰")
    await asyncio.sleep(1.5)
    await casino_message.reply("Ваш выигрыш "+str(message.from_user.first_name)+": "+str(casino_message.dice.value))

@dp.message(Command("bouling"))
async def casino_command(message: types.Message):
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    bouling_message = await bot.send_dice(message.chat.id, emoji="🎳")
    await asyncio.sleep(1.5)
    await bouling_message.reply("Ваш выигрыш "+str(message.from_user.first_name)+": "+str(bouling_message.dice.value))

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
    

"""""
@dp.message(Command("repeat"))
async def cmd_repeat(message: types.Message):
	prompte = message.text.replace("/repeat", "").strip()
	if not prompte:
		await message.reply(f"{message.from_user.first_name} вы отправили пустое сообщение!")
		return
	else:
		await bot.send_message(message.chat.id, text=f"{prompte}")
		await bot.delete_message(message.chat.id, message.message_id)
"""""

@dp.message(Command("report"))
async def report_com(message: types.Message):
    text = str(message.text).replace("/report ","").replace("/report","")
    if str(text).replace(" ","")!="":
        Name = str(text).split()[0]
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        NameAndLastname = ""
        if message.from_user.first_name != None:
            NameAndLastname += str(message.from_user.first_name)+" "
        if message.from_user.last_name != None:
            NameAndLastname += str(message.from_user.last_name)+" "
        NameAndLastname += "("+str(message.from_user.username)+")"
        text = text.replace(f"{Name} ", "")
        text = "🛑 РЕПОРТ! 🛑\n\nПользователь: "+str(NameAndLastname)+" c ID: "+str(message.from_user.id)+"\nПожаловался на пользователя "+str(Name)+"\n\nПричина: "+str(text)
        try:
            try:
                await bot.send_message(1828269322, text=text)  # ЕГОР: 5038019526 #АНТОН: 1828269322
            except:
                pass
            await bot.send_message(5038019526, text=text) #ЕГОР: 5038019526 #АНТОН: 1828269322
        except:
            await bot.send_message(message.chat.id, text="🛑 Невозможно отправить репорт, т.к у админа нет активного чата с ботом 🛑")
    else:
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        await bot.send_message(message.chat.id, text="🛑 Вы не можете отправить пустую жалобу! 🛑")

"""""
@dp.message(Command("myinfo"))
async def cmd_myinfo(message: types.Message):
	AllInfo = f"Вот некоторая информация о вас:\n\nID: {message.from_user.id}"
	if message.from_user.first_name == None:
		AllInfo += f"\nИмя: ❌"
	else:
		AllInfo += f"\nИмя: {message.from_user.first_name}"

	if message.from_user.last_name == None:
		AllInfo += f"\nФамилия: ❌"
	else:
		AllInfo += f"\nФамилия: {message.from_user.last_name}"

	if message.from_user.username == None:
		AllInfo += f"\nИмя пользователя: ❌"
	else:
		AllInfo += f"\nИмя пользователя: {message.from_user.username}"

	if message.from_user.language_code == None:
		AllInfo += f"\nЯзыковой код: ❌"
	else:
		AllInfo += f"\nЯзыковой код: {message.from_user.language_code}"

	if message.from_user.is_premium == None:
		AllInfo += f"\nПремиум: ❌"
	else:
		AllInfo += f"\nПремиум: ✔️"

	await message.reply(AllInfo)
"""""

@dp.message(lambda message: message.from_user.id)
async def reestr(message: types.Message):
    try:
        if str(message.sticker.file_id) == "CAACAgIAAyEFAAS-sUXhAAICsGj82mZGFkD4z_8DMScm5QmvN_8uAAJ7egACL83ZS5UMSiKceRpVNgQ":
            sumbantime = 10
            await message.reply("бан на "+str(sumbantime)+" мин")
            now = datetime.datetime.now()
            ban_until = now + timedelta(minutes=sumbantime)
            timestamp = int(ban_until.timestamp())
            await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=types.ChatPermissions(),
                    until_date=timestamp)
    except:
        sumbantime = 0
        text = str(message.text).lower()
        text = str(''.join(e for e in text if e.isalnum()))
        text = str(re.sub(r'([а-я])\1+', r'\1', text))
        text = str(re.sub(r'([a-z])\1+', r'\1', text))
        for i in text.split():
            i = str(i)
            for i1 in blockSlova:
                i1 = str(i1)
                #print(str(i1)+" "+str(int(round(ratio(i, i1)*100))))
                if int(round(ratio(i, i1)*100)) > 86:
                    sumbantime+=5
                    text.replace(i," ")
                    break
        for i in blockSlova:
            if i in text:
                sumbantime+=5
                text.replace(i1," ")
        if int(sumbantime)>0:
            await message.reply("бан на "+str(sumbantime)+" мин")
            now = datetime.datetime.now()
            ban_until = now + timedelta(minutes=sumbantime)
            timestamp = int(ban_until.timestamp())
            try:
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=types.ChatPermissions(),
                    until_date=timestamp)
            except:
                pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


