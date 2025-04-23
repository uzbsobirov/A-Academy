from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.inline.panel import required1, required2
from loader import db, bot
from states.panel import AdminState
from utils.misc.checking import check_is_admin


router = Router()


@router.callback_query(StateFilter(AdminState.main), F.data == "majburiy")
async def settings_required(call: types.CallbackQuery, state: FSMContext):
    all_channels = await db.select_all_sponsors()

    txt = "<b>Majburiy obuna ulangan kanallar👇\n\n</b>"
    count = 1

    if len(all_channels) == 0:
        text = "<b>Majburiy obuna ulanmagan🙅‍♂️</b>"
        await call.message.edit_text(text=text, reply_markup=required1)
    else:
        for item in all_channels:
            txt += f"{count}) <code>{item[0]}</code> | <a href='{item[4]}'>{item[1]}</a>\n"
            count += 1
        txt += f"<b>Kanalni o'chirish uchun 'id' sini yuboring, Masalan: {all_channels[0][0]}</b>"
        await call.message.edit_text(text=txt, reply_markup=required2, disable_web_page_preview=True)

    await state.set_state(AdminState.sponsors)


@router.callback_query(StateFilter(AdminState.sponsors), F.data == "add_channel")
async def settings_required(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Kanal qo'shish uchun kanaldan birorta xabarni 'forward' qilib yuboring\n\n"
                                      "❗️Bot kanalda yoki guruhda admin bo'lgan bo'lishi shart</b>")
    await state.set_state(AdminState.get_channel)


@router.message(StateFilter(AdminState.get_channel))
async def get_channel_info(message: types.Message, state: FSMContext):
    data = await bot.get_me()
    bot_username = data.username

    chat_id = message.forward_from_chat.id
    channel_name = message.forward_from_chat.title
    username = message.forward_from_chat.username

    get_channel_data = await bot.get_chat(chat_id=chat_id)

    try:
        checking = await check_is_admin(chat_id=chat_id)
        for item in checking:
            if item.user.username == bot_username and item.status == "administrator":
                await message.answer(text="Majburiy obuna ro'yhatiga qo'shildi✅")
    except (Unauthorized, BadRequest) as UB:

    print(chat_id, channel_name, username)
    print(message)


