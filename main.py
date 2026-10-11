import os
os.system("pip install requests")
os.system("pip install bs4")
os.system("pip install aiogram")
import asyncio
import random
from datetime import timedelta
import datetime
import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.types import ChatPermissions

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("info"))
async def info_command(message: types.Message):
    sender_status = await message.chat.get_member(message.from_user.id)
    if sender_status.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply(text=
            "Вот все команды, по которым вы можете обращаться ко мне:\n\n"
            "/criminal --- Узнать свою статью УК РФ\n"
            "/dice --- Бросить кубик\n"
            "/bouling --- Боулинг\n"
            "/target --- Попасть в мишень\n"
            "/casino --- Играть в казино\n"
            "/report [@провинившийся] [причина] --- Кинуть жб\n"
            "/info --- Информация о командах\n\n"
            "----АДМИН КОМАНДЫ----\n"
            "[reply на сообщение] /ban [время бана в МИН] --- Забанить\n"
            "[reply на сообщение] /unban --- Разбанить")
    else:
        await message.reply(text=
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
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    dice_message = await bot.send_dice(chat_id=message.chat.id, emoji="🎲")
    await dice_message.reply(text=f"{message.from_user.first_name}, вам выпало число: {dice_message.dice.value}")

@dp.message(Command("target"))
async def target_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    target_messages = await bot.send_dice(chat_id=message.chat.id, emoji="🎯")
    await target_messages.reply(text=f"{message.from_user.first_name}, вы попали в число: {target_messages.dice.value}")

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    casino_message = await bot.send_dice(chat_id=message.chat.id, emoji="🎰")
    await casino_message.reply(text=f"Ваш выигрыш {message.from_user.first_name}: {casino_message.dice.value}")

@dp.message(Command("bouling"))
async def bouling_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    bouling_message = await bot.send_dice(message.chat.id, emoji="🎳")
    await bouling_message.reply(text=f"Ваш выигрыш {message.from_user.first_name}: {bouling_message.dice.value}")

@dp.message(Command("criminal"))
async def criminal_command(message: types.Message):
    while True:
        url = "https://rulaws.ru/uk/?ysclid=mh0o16yda4718036120"
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, "html.parser")
        vibor = random.randint(143, len(soup.find("table").find_all("tr")))
        if "Глава" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "Раздел" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","") and "ЧАСТЬ ОБЩАЯ" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n","")  and "Утратила силу" not in str(soup.find("table").find_all("tr")[vibor].text).replace("\n",""):
            await message.reply(text="👤 "+str(message.from_user.username)+" обвиняется по "+str(soup.find("table").find_all("tr")[vibor].text).replace("\n","").replace("Статья","статье ⚖️")+" 🔗")
            break

@dp.message(Command("report"))
async def report_command(message: types.Message):
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
                await bot.send_message(chat_id=1828269322, text=report_text)
            except Exception:
                pass
            await bot.send_message(chat_id=2021260772, text=report_text)
        except Exception:
            await message.answer(text="🛑 Невозможно отправить репорт, т.к. у админа нет активного чата с ботом 🛑")
    else:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception:
            pass
        await message.answer(text="🛑 Вы не можете отправить пустую жалобу! 🛑")

async def ban(message, ban_time):
    await bot.send_message(text=f"<blockquote> {message.reply_to_message.from_user.username} </blockquote>\n🔒 Бан на {ban_time} мин !", chat_id=message.chat.id, parse_mode=ParseMode.HTML)
    now = datetime.datetime.now()
    ban_until = now + timedelta(minutes=ban_time)
    timestamp = int(ban_until.timestamp())
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=types.ChatPermissions(), until_date=timestamp)

async def unban(message):
    await bot.send_message(text=f"<blockquote> {message.reply_to_message.from_user.username} </blockquote>\n🔓 {random.choice(['Разбанен','Холоп свободен','Нищита освобождена'])}", chat_id=message.chat.id, parse_mode=ParseMode.HTML)
    await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=True,can_send_audios=True,can_send_documents=True,can_send_photos=True,can_send_videos=True,can_send_video_notes=True,can_send_voice_notes=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True,can_change_info=False,can_invite_users=True,can_pin_messages=True))

@dp.message(Command("ban"))
async def report_com(message: types.Message, command: CommandObject):
    sender_status = await message.chat.get_member(message.from_user.id)
    if sender_status.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply(text="❌ Отказано нищита")
        return
    await bot.delete_message(message.chat.id, message.message_id)
    await ban(message=message, ban_time=float(str(command.args).split()[0]))

@dp.message(Command("unban"))
async def report_com(message: types.Message):
    sender_status = await message.chat.get_member(message.from_user.id)
    if sender_status.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply(text="❌ Отказано нищита")
        return
    await bot.delete_message(message.chat.id, message.message_id)
    await unban(message=message)
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(main())
    except RuntimeError:
        asyncio.run(main())
