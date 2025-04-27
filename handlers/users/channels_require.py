from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Union

from asyncpg import UniqueViolationError

from keyboards.inline.channels import channels_func
from keyboards.inline.main_buttons import main
from keyboards.inline.panel import required1, required2, admin
from loader import db, bot
from states.panel import AdminState
# from utils.misc.checking import check_is_admin


router = Router()


async def check_is_admin(chat_id: Union[str, int]):
    member = await bot.get_chat_administrators(chat_id=chat_id)
    return member


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
        txt += f"<b>\nKanalni o'chirish uchun 'id' sini yuboring, Masalan: {all_channels[0][0]}</b>"
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
    name = message.forward_from_chat.title
    username = message.forward_from_chat.username

    try:
        chat_link = await bot.export_chat_invite_link(chat_id=chat_id)

        checking = await check_is_admin(chat_id=chat_id)
        for item in checking:
            if item.user.username == bot_username and item.status == "administrator":
                await db.add_sponsor(
                    name=name,
                    username=username,
                    chat_id=chat_id,
                    invite_link=chat_link
                )
                await message.answer(text="Majburiy obuna ro'yhatiga qo'shildi✅", reply_markup=admin)
                await state.set_state(AdminState.main)
    except TelegramForbiddenError as error:
        print(error)
        await message.answer(text="<b>Bot kanal yoki guruhda admin emas, iltimos oldin admin qilib "
                                  "keyin qaytadan urinib ko'ring</b>")

    except UniqueViolationError as UVE:
        print(UVE)
        await message.answer(text="<b>Bu kanal allaqachon majburiy obuna ro'yhatida mavjud</b>")


# //////// DELETE THE REQUIRED CHANNEL ////////
@router.callback_query(StateFilter(AdminState.sponsors), F.data == "delete_channel")
async def delete_channel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Yaxshi, o'chirmoqchi bo'lgan kanalingiz 'id' sini yuboring</b>")
    await state.set_state(AdminState.delete_sponsor)


@router.message(StateFilter(AdminState.delete_sponsor))
async def get_deleted_channel(message: types.Message, state: FSMContext):
    id = message.text
    try:
        await db.delete_sponsor(id=int(id))
        await message.answer(text="<b>Kanal majburiy obuna ro'yhatidan o'chirib tashlandi✅</b>", reply_markup=admin)
        await state.set_state(AdminState.main)

    except ValueError as VE:
        print(VE)
        await message.answer(text="<b>Iltimos, faqat sonlardan foydalaning!</b>")
        await state.set_state(AdminState.delete_sponsor)


# /////// CHECKING BUTTON //////
@router.callback_query(F.data == "check_subs")
async def check_subscription_status(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    # 🔁 Fetch channels from DB
    db_channels = await db.select_all_sponsors()

    unsubscribed_channels = []
    unsubscribed_urls = []

    for row in db_channels:
        channel_id = row["chat_id"]
        member = await call.bot.get_chat_member(channel_id, user_id)

        if member.status == "left":
            chat = await call.bot.get_chat(channel_id)
            unsubscribed_channels.append(channel_id)
            unsubscribed_urls.append(chat.invite_link)

    if unsubscribed_channels:
        text = "<b>❌ Siz hali quyidagi kanallarga a'zo bo'lmagansiz:</b>"
        await call.message.edit_text(
            text=text,
            reply_markup=channels_func(len(unsubscribed_channels), url=unsubscribed_urls)
        )
    else:
        await call.message.edit_text(
            "<b>✅ Siz barcha kanallarga a'zo bo'lgansiz. Botdan foydalanishingiz mumkin!</b>",
            reply_markup=main
        )
        await state.clear()