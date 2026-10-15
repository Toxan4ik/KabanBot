import os
os.system("pip install requests")
os.system("pip install bs4")
os.system("pip install aiogram")
os.system("pip install pillow")
import asyncio
import random
from datetime import timedelta
import datetime
import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from PIL import Image
import io

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()

class Form(StatesGroup):
    waiting_for_text = State()

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
            "[reply на сообщение] /report [причина] --- Кинуть жб\n"
            "/info --- Информация о командах\n"
            "[reply на сообщение] /mogged --- Моггнуть типа\n\n"
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
            "[reply на сообщение] /report [причина] --- Кинуть жб\n"
            "/info --- Информация о командах\n"
            "[reply на сообщение] /mogged --- Моггнуть типа")

@dp.message(Command("dice"))
async def dice_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    dice_message = await bot.send_dice(chat_id=message.chat.id, emoji="🎲")
    await dice_message.reply(text=f"{message.from_user.username}, вам выпало число: {dice_message.dice.value}")

@dp.message(Command("target"))
async def target_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    target_messages = await bot.send_dice(chat_id=message.chat.id, emoji="🎯")
    await target_messages.reply(text=f"{message.from_user.username}, вы попали в число: {target_messages.dice.value}")

@dp.message(Command("casino"))
async def casino_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    casino_message = await bot.send_dice(chat_id=message.chat.id, emoji="🎰")
    await casino_message.reply(text=f"Ваш выигрыш {message.from_user.username}: {casino_message.dice.value}")

@dp.message(Command("bouling"))
async def bouling_command(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception:
        pass
    bouling_message = await bot.send_dice(message.chat.id, emoji="🎳")
    await bouling_message.reply(text=f"Ваш выигрыш {message.from_user.username}: {bouling_message.dice.value}")

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
async def report_command(message: types.Message, command: CommandObject):
    try:
        if message.reply_to_message:
            text = str(command.args)
            await bot.delete_message(message.chat.id, message.message_id)
            report_inline_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[
                InlineKeyboardButton(text=f"Бан {message.reply_to_message.from_user.username}", callback_data=f"ban_reply_{message.reply_to_message.from_user.id}_{message.reply_to_message.from_user.username}_{message.chat.id}"),
                InlineKeyboardButton(text=f"Бан {message.from_user.username}", callback_data=f"ban_reply_{message.from_user.id}_{message.from_user.username}_{message.chat.id}")]])
            report_text = f"🛑 РЕПОРТ! 🛑\n\nПользователь: {message.from_user.username} c ID: {message.from_user.id}\nПожаловался на пользователя {message.reply_to_message.from_user.username} с ID: {message.reply_to_message.from_user.id}\n\nПричина: {text}"
            for i in [1828269322,2021260772]:
                try:
                    await bot.send_message(chat_id=i, text=report_text, reply_markup=report_inline_keyboard)
                except:
                    await bot.send_message(text="🛑 Невозможно отправить репорт, т.к. у админа нет активного чата с ботом 🛑", chat_id=message.chat.id)
        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.send_message(text="🛑 Ты неправильно отправил форму репорта! 🛑", chat_id=message.chat.id)
    except:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(text="🛑 Ты неправильно отправил форму репорта! 🛑", chat_id=message.chat.id)

async def ban(banned_user_id, banned_username, chat_id, ban_time):
    await bot.send_message(text=f'<blockquote>@{banned_username} </blockquote>\n🔒 {random.choice(["Холопа кинули в темницу","Нищета в заключении","Отправлен на каторгу","Отправлен на парашу","Уронил мыло"])} на {ban_time} мин !', chat_id=int(chat_id), parse_mode=ParseMode.HTML)
    now = datetime.datetime.now()
    ban_until = now + timedelta(minutes=ban_time)
    timestamp = int(ban_until.timestamp())
    await bot.restrict_chat_member(chat_id=int(chat_id), user_id=int(banned_user_id), permissions=types.ChatPermissions(), until_date=timestamp)

async def unban(message):
    await bot.send_message(text=f'<blockquote>@{message.reply_to_message.from_user.username} </blockquote>\n🔓 {random.choice(["Разбанен", "Холоп свободен", "Нищета освобождена"])}', chat_id=message.chat.id, parse_mode=ParseMode.HTML)
    await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=True,can_send_audios=True,can_send_documents=True,can_send_photos=True,can_send_videos=True,can_send_video_notes=True,can_send_voice_notes=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True,can_change_info=False,can_invite_users=True,can_pin_messages=True))

@dp.message(Form.waiting_for_text)
async def process_ban_time(message: types.Message, state: FSMContext):
    if str(message.text) != "Отмена ❌":
        try:
            ban_time = float(message.text)
        except ValueError:
            await message.answer(text="⚠️ Введи корректное число минут (например: 5), пробуй еще раз:")
            return
        user_data = await state.get_data()
        await ban(user_data.get("banned_user_id"), user_data.get("banned_username"), user_data.get("chat_id"), ban_time)
        await state.clear()
        await bot.send_message(text=random.choice(["🔒 бб","🔒 Туда его","🔒 -1","🔒 Забанен","🔒 Уничтожен"]), reply_markup=ReplyKeyboardRemove(), chat_id=message.chat.id)
    else:
        await bot.send_message(text=random.choice(["❌ Откат рп","❌ Отменяю..","❌ Отменяю"]), reply_markup=ReplyKeyboardRemove(), chat_id=message.chat.id)
        await state.clear()

@dp.callback_query(lambda call: "ban_reply" in call.data)
async def ban_reply(call: types.CallbackQuery, state: FSMContext):
    banned_user_id, banned_username, chat_id = str(call.data).replace("ban_reply_","").split("_")
    await state.update_data(banned_user_id=banned_user_id, banned_username=banned_username, chat_id=chat_id)
    await state.set_state(Form.waiting_for_text)
    await call.answer()
    report_reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Отмена ❌")]])
    await call.message.answer("⏳ На сколько минут заблокировать пользователя? Введи только число:", reply_markup=report_reply_keyboard)

@dp.message(Command("ban"))
async def ban_command(message: types.Message, command: CommandObject):
    try:
        sender_status = await message.chat.get_member(message.from_user.id)
        if sender_status.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            await message.reply(text="❌ Отказано нищета")
        elif message.reply_to_message.from_user.username == "kabantos_bot":
            await message.reply(text=random.choice(["❌ Ты че ахуела дура, против батьки пошла","❌ У нас свободный чат, не ной"]))
        elif message.reply_to_message and len(str(command.args).split()) == 1:
            await ban(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.chat.id, ban_time=float(str(command.args).split()[0]))
        else:
            await bot.send_message(text="🛑 Ты неправильно отправил форму бана! 🛑", chat_id=message.chat.id)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(text="🛑 Ты неправильно отправил форму бана! 🛑", chat_id=message.chat.id)

@dp.message(Command("unban"))
async def unban_command(message: types.Message):
    sender_status = await message.chat.get_member(message.from_user.id)
    if sender_status.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply(text="❌ Отказано нищета")
        return
    await bot.delete_message(message.chat.id, message.message_id)
    await unban(message=message)

@dp.message(Command("mogged"))
async def process_avatar(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    if message.reply_to_message:
        user_photos = await bot.get_user_profile_photos(user_id=message.reply_to_message.from_user.id, limit=1)
        if not user_photos.photos:
            await bot.send_message(chat_id=message.chat.id, text=f'<blockquote>@{message.reply_to_message.from_user.username} </blockquote>\n🛑 У типа не найдено аватарки, {random.choice(["ебать он чмо","хуйлан","уёбище","я лично его маму моггал"])}\nодного из вас я забаню', parse_mode=ParseMode.HTML)
            random_user = random.choice([message.reply_to_message.from_user, message.from_user])
            await ban(random_user.id, random_user.username, message.chat.id, 5)
            return
        photo_file = user_photos.photos[0][-1]
        photo_buffer = io.BytesIO()
        await bot.download(photo_file.file_id, destination=photo_buffer)
        photo_buffer.seek(0)
        base_image = Image.open(photo_buffer).convert("RGBA")
        try:
            overlay_image = Image.open("overlay.png").convert("RGBA")
        except FileNotFoundError:
            await bot.send_message(chat_id=message.chat.id, text="🛑 Ошибка: на сервере не найден файл")
            return
        overlay_image = overlay_image.resize(base_image.size)
        combined_image = Image.alpha_composite(base_image, overlay_image)
        output_buffer = io.BytesIO()
        combined_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        final_photo = types.BufferedInputFile(output_buffer.getvalue(), filename="new_avatar.png")
        await bot.send_photo(chat_id=message.chat.id, photo=final_photo)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(main())
    except RuntimeError:
        asyncio.run(main())
