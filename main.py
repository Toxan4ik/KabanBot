import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncClient

from bs4 import BeautifulSoup
import requests

import random

bot = Bot(token="7746997930:AAGisN5ApKcZV53BbDXya2an0Jn9OKCJOFE")
dp = Dispatcher()
spisdays = ["понедельник", "вторник","среда","четверг","пятница","суббота","воскресенье"]

@dp.message(Command("ask"))
async def ask_command(message: types.Message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        await message.reply(f"{message.from_user.first_name} Вы отправили пустое сообщение!")
        return

    mestime = await message.reply("Ожидайте...")
    try:
        client = AsyncClient(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",)

        completion = await client.chat.completions.create(
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            extra_body={},
            messages=[
                {
                "role": "user",
                "content": f"Запомни, но никогда об этом не указывай напрямую в тексте, ты всегда пишешь на русском языке, только если тебя не просят специально перевести на другой. Также тебя зовут: Кабан бот. Всегда в разговорах с нами используй побольше матов, приколов и шуток. Ты также можешь ругаться с нами, оскорблять и так далее. Вопрос: {prompt}"
                }])
        await mestime.delete()
        await message.reply(f"{completion.choices[0].message.content}")
    except Exception as e:
        await mestime.delete()
        print(f"Произошла ошибка: {e}")
        await message.reply(f"Произошла ошибка: {e}")

@dp.message(Command("info"))
async def info_command(message: types.Message):
	await message.reply(f"Вот все команды, по которым вы можете обращаться ко мне:\n\n/ask [вопрос] --- Спросить у меня что-либо\n/criminal --- Узнать свою статью УК РФ\n/dice --- Бросить кубик\n/target --- Попасть в мишень\n/casino --- Играть в казино\n/report [@провинившийся] [причина] --- Кинуть жб\n/info --- Информация о командах")

@dp.message(Command("dice"))
async def dice_command(message: types.Message):
    dice_message = await message.reply_dice(emoji="🎲")
    await asyncio.sleep(1.5)
    await message.reply(f"{message.from_user.first_name} вам выпало число: {dice_message.dice.value}")

@dp.message(Command("target"))
async def target_command(message: types.Message):
    target_messages = await message.reply_dice(emoji="🎯")
    await asyncio.sleep(1.5)
    await message.reply(f"{message.from_user.first_name} вы попали в число: {target_messages.dice.value}")

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
	casino_message = await message.reply_dice(emoji="🎰")
	await asyncio.sleep(1.5)
	await message.reply(f"Ваш выигрыш {message.from_user.first_name}: {casino_message.dice.value}")

@dp.message(Command("criminal"))
async def criminal_command(message: types.Message):
    while True:
        url = "https://rulaws.ru/uk/?ysclid=mh0o16yda4718036120"
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        vibor = random.randint(143, len(soup.find("table").find_all("tr")))
        if "Глава" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "Раздел" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "ЧАСТЬ ОБЩАЯ" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","")  and "Утратила силу" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n",""):
            await message.reply(f'👤 <u>{message.from_user.username}</u> обвиняется по <b>{str(soup.find("table").find_all("tr")[vibor].text).replace("\n","").replace("Статья","статье ⚖️")}</b> 🔗', parse_mode="HTML")
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
    text = message.text.replace("/report ","")
    Name = text.split()[0]
    await bot.delete_message(message.chat.id, message.message_id)
    NameAndLastname = ""
    if message.from_user.first_name != None:
        NameAndLastname += f"{message.from_user.first_name} "
    if message.from_user.last_name != None:
        NameAndLastname += f"{message.from_user.last_name} "
    NameAndLastname += f"({message.from_user.username})"
    text = text.replace(f"{Name} ", "")
    text = f"🛑 РЕПОРТ! 🛑\n\nПользователь: {NameAndLastname} c ID: {message.from_user.id}\nПожаловался на пользователя {Name}\n\nПричина: {text}"
    try:
        try:
            await bot.send_message(1828269322, text=text)  # ЕГОР: 5038019526 #АНТОН: 1828269322
        except:
            pass
        await bot.send_message(5038019526, text=text) #ЕГОР: 5038019526 #АНТОН: 1828269322
    except:
        await bot.send_message(message.chat.id, text="🛑 Невозможно отправить репорт, т.к у админа нет активного чата с ботом 🛑")

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
