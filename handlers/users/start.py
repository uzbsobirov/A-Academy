from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from aiogram.fsm.context import FSMContext
from states.simple import GetName

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user = None
    try:
        user = await db.add_user(user_id=user_id, full_name=None, username=username)
    except Exception as error:
        logger.info(error)
    if user:
        count = await db.count_users()
        msg = (f"[{make_title(user['full_name'])}](tg://user?id={user['user_id']}) bazaga qo'shildi\.\n"
               f"Bazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"[{make_title(full_name)}](tg://user?id={user_id}) bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    await message.answer(f"<b>📝Ism va familyangizni kiriting. Iltimos to'g'ri va to'liq yozing. "
                         f"Lotin harflaridan foydalaning !</b>")


@router.message()
async def get_name(message: types.Message):
    user_id = message.from_user.id
    user_info = await db.select_one_user(user_id)
    print(user_info)
    name = message.text

    text = f"<b>📝Ism va familyangizni kiriting. Iltimos to'g'ri va to'liq yozing. Lotin harflaridan foydalaning !</b>"

    if len(name.split()) == 2:
        await db.update_user_name(full_name=name, user_id=user_id)
    else:
        await message.answer(text=text)



