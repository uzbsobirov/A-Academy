from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from aiogram.fsm.context import FSMContext
from states.simple import GetName
from keyboards.inline.main_buttons import main

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user_mention = f"[{make_title(full_name)}](tg://user?id={user_id})"
    user = None
    try:
        user = await db.add_user(user_id=user_id, full_name=None, username=username)
    except Exception as error:
        logger.info(error)
    if user:
        count = await db.count_users()
        msg = (f"{user_mention} bazaga qo'shildi\.\n"
               f"Bazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"{user_mention} bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    user_info = await db.select_one_user(user_id)
    if user_info[1] is None:
        await message.answer(f"<b>📝Ism va familyangizni kiriting. Iltimos to'g'ri va to'liq yozing. "
                         f"Lotin harflaridan foydalaning !</b>")
        await state.set_state(GetName.name)
    else:
        user_mention = f"<a href='tg://user?id={user_info['user_id']}'>{user_info[1]}</a>"
        text = f"""<b>👤Hurmatli {user_mention} botimizga xush kelibsiz</b>"""
        await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=main)
        await state.clear()


@router.message(GetName.name)
async def get_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text

    text = f"<b>📝Ism va familyangizni kiriting. Iltimos to'g'ri va to'liq yozing. Lotin harflaridan foydalaning !</b>"

    if len(name.split()) == 2:
        await db.update_user_name(full_name=name, user_id=user_id)
        user_info = await db.select_one_user(user_id)
        user_mention = f"<a href='tg://user?id={user_info['user_id']}'>{user_info[1]}</a>"
        text = f"""<b>👤Hurmatli {user_mention} botimizga xush kelibsiz</b>"""
        await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=main)
        await state.clear()
    else:
        await message.answer(text=text)
        await state.set_state(GetName.name)





