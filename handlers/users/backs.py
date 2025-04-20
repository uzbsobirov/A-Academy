from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.simple import HowAnswer
from loader import db
from keyboards.inline.main_buttons import main

router = Router()


@router.callback_query(StateFilter(HowAnswer.about), F.data == "back")
async def main_back(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_info = await db.select_one_user(user_id)

    user_mention = f"<a href='tg://user?id={user_info['user_id']}'>{user_info[1]}</a>"
    text = f"""<b>👤Hurmatli {user_mention} botimizga xush kelibsiz</b>"""

    await call.message.edit_text(text=text, parse_mode=ParseMode.HTML, reply_markup=main)
    await state.clear()
