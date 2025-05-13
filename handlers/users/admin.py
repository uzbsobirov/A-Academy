import logging
import asyncio
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import date, datetime, timedelta

from keyboards.inline.backs import back
from keyboards.inline.panel import admin
from loader import db, bot
from keyboards.inline.buttons import are_you_sure_markup
from states.panel import AdminState
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel

router = Router()


async def get_admin_ids():
    result = await db.select_all_admins()

    # Extract user IDs from the result (assuming the result is a list of dicts)
    admin_ids = [row['user_id'] for row in result]

    return admin_ids


@router.message(Command('allusers'), IsBotAdminFilter(get_admin_ids))
async def get_all_users(message: types.Message):
    users = await db.select_all_users()

    file_path = f"data/users_list.xlsx"
    await export_to_excel(data=users, headings=['ID', 'Full Name', 'Username', 'Telegram ID'], filepath=file_path)

    await message.answer_document(types.input_file.FSInputFile(file_path))


@router.callback_query(StateFilter(AdminState.main), F.data == "send_ads")
async def ask_ad_content(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>Reklama uchun post yuboring</b>")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    count = 0
    for user in users:
        user_id = user[-1]
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"<b>Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.</b>")
    await message.answer(text="<b>Admin panel</b>", reply_markup=admin)
    await state.set_state(AdminState.main)


@router.message(Command('cleandb'), IsBotAdminFilter(get_admin_ids))
async def ask_are_you_sure(message: types.Message, state: FSMContext):
    msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?", reply_markup=are_you_sure_markup)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.are_you_sure)


@router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(get_admin_ids))
async def clean_db(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        await db.delete_users()
        text = "Baza tozalandi!"
    elif call.data == 'no':
        text = "Bekor qilindi."
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    await state.clear()


@router.message(Command('panel'), IsBotAdminFilter(get_admin_ids))
async def admin_panel(message: types.Message, state: FSMContext):
    text = "*Admin panelga xush kelibsiz*"

    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=admin)
    await state.set_state(AdminState.main)


@router.callback_query(StateFilter(AdminState.main), F.data == "statistic")
async def statistics(call: types.CallbackQuery, state: FSMContext):
    get_me = await bot.get_me()
    bot_username = get_me.username

    todays_date = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    all_users = await db.select_all_users()
    text = "<b>📅 Bugungi sana: {}\n" \
           "🕰 Hozirgi vaqt: {}\n\n" \
           "📊 Bot obunachilari soni: {}\n\n" \
           "⚡️ @{}</b>".format(todays_date, current_time, len(all_users), bot_username)

    await call.message.edit_text(text=text, reply_markup=back)
    await state.set_state(AdminState.statistic)