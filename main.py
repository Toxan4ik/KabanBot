from os import system

system("pip install openai")
system("pip install bs4")
system("pip install lxml")
system("pip install asyncio")

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncClient

from bs4 import BeautifulSoup
import requests

import random

bot = Bot(token="7746997930:AAGisN5ApKcZV53BbDXya2an0Jn9OKCJOFE") # кабан 7746997930:AAGisN5ApKcZV53BbDXya2an0Jn9OKCJOFE   погода 7783613623:AAHHSWVi7HlB6PhX2rEmJeFNCZKMXO7UJGI
dp = Dispatcher()
spisdays = ["понедельник", "вторник","среда","четверг","пятница","суббота","воскресенье"]

@dp.message(Command("ask"))
async def ask_command(message: types.Message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        await message.reply(str(message.from_user.first_name)+" вы отправили пустое сообщение!")
        return

    mestime = await message.reply("Ожидайте...")
    try:
        client = AsyncClient(
            base_url="https://openrouter.ai/api/v1",
            api_key=super_secret: ${{ secrets.APIROUTER }},)

        completion = await client.chat.completions.create(
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            extra_body={},
            messages=[
                {
                "role": "user",
                "content": "Запомни, но никогда об этом не указывай напрямую в тексте, ты всегда пишешь на русском языке, только если тебя не просят специально перевести на другой. Также тебя зовут: Кабан бот. Всегда в разговорах с нами используй побольше матов, приколов и шуток. Ты также можешь ругаться с нами, оскорблять и так далее. Вопрос: "+prompt
                }])
        await mestime.delete()
        await message.reply(completion.choices[0].message.content)
    except Exception as e:
        await mestime.delete()
        print("Произошла ошибка: "+str(e))
        await message.reply("Произошла ошибка: "+str(e))

@dp.message(Command("info"))
async def info_command(message: types.Message):
	await message.reply("Вот все команды, по которым вы можете обращаться ко мне:\n\n/ask [вопрос] --- Спросить у меня что-либо\n/criminal --- Узнать свою статью УК РФ\n/dice --- Бросить кубик\n/target --- Попасть в мишень\n/casino --- Играть в казино\n/report [@провинившийся] [причина] --- Кинуть жб\n/info --- Информация о командах")

@dp.message(Command("dice"))
async def dice_command(message: types.Message):
    dice_message = await message.reply_dice(emoji="🎲")
    await asyncio.sleep(1.5)
    await message.reply(str(message.from_user.first_name)+" вам выпало число: "+str(dice_message.dice.value))

@dp.message(Command("target"))
async def target_command(message: types.Message):
    target_messages = await message.reply_dice(emoji="🎯")
    await asyncio.sleep(1.5)
    await message.reply(str(message.from_user.first_name)+" вы попали в число: "+str(target_messages.dice.value))

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
	casino_message = await message.reply_dice(emoji="🎰")
	await asyncio.sleep(1.5)
	await message.reply("Ваш выигрыш "+str(message.from_user.first_name)+": "+str(casino_message.dice.value))

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
    text = message.text.replace("/report ","").replace("/report","")
    if str(text).replace(" ","")!="":
        Name = text.split()[0]
        await bot.delete_message(message.chat.id, message.message_id)
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
        await bot.delete_message(message.chat.id, message.message_id)
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





