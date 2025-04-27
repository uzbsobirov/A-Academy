from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from asyncpg import UniqueViolationError

from keyboards.inline.panel import settings_admins, admin
from loader import db, bot
from states.panel import AdminState

router = Router()


@router.callback_query(StateFilter(AdminState.main), F.data == "admins_list")
async def admins_lst(call: types.CallbackQuery, state: FSMContext):
    admins_list = await db.select_all_admins()

    text = "<b>Botdagi adminlar👇\n\n</b>"
    count = 1

    for item in admins_list:
        user_mention = f"<a href='tg://user?id={item['user_id']}'>{item['name']}</a>"
        text += f"{count}) {user_mention} | 🆔: <code>{item['user_id']}</code>\n"
        count += 1

    await call.message.edit_text(text=text, reply_markup=settings_admins)

    await state.set_state(AdminState.admins)


# /////// ADD ADMIN //////
@router.callback_query(StateFilter(AdminState.admins), F.data == "add_admin")
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    text = "<b>Qo'shmoqchi bo'lgan adminingizdan birorta xabarni 'forward' qilib yuboring</b>"
    await call.message.edit_text(text=text)
    await state.set_state(AdminState.adding_admin)


@router.message(StateFilter(AdminState.adding_admin))
async def addd_admin(message: types.Message, state: FSMContext):

    try:
        user_id = message.forward_from.id
        name = message.forward_from.full_name
        username = message.forward_from.username

        await db.add_admin(name=name, username=username, user_id=user_id)
        user_mention = f"<a href='tg://user?id={user_id}'>{name}</a>"
        await message.answer(text=f"{user_mention} <b>adminlar ro'yhatiga qo'shildi✅</b>", reply_markup=admin)
        await state.set_state(AdminState.main)

    except UniqueViolationError as UVE:
        print(UVE)
        await message.answer(text="<b>Bu foydalanuvchi allaqachon adminlar ro'yhatiga qo'shilgan</b>")
        await state.set_state(AdminState.adding_admin)

    except AttributeError as AE:
        print(AE)
        await message.answer(text="<b>Iltimos, faqat foydalanuvchilardan 'forward' habarlar yuboring</b>")
        await state.set_state(AdminState.adding_admin)


# ///// DELETE ADMIN /////
@router.callback_query(StateFilter(AdminState.admins), F.data == "delete_admin")
async def delete_admins(call: types.CallbackQuery, state: FSMContext):
    text = "<b>O'chirmoqchi bo'lgan adminingiz idsini kiriting</b>\n\n"
    admins_list = await db.select_all_admins()

    count = 1

    for item in admins_list:
        user_mention = f"<a href='tg://user?id={item['user_id']}'>{item['name']}</a>"
        text += f"{count}) {user_mention} | 🆔: <code>{item['user_id']}</code>\n"
        count += 1

    text += "<b>\nID ni ustiga bossangiz avto copy qiladi❗️</b>"
    await call.message.edit_text(text=text)
    await state.set_state(AdminState.delete_admin)


@router.message(StateFilter(AdminState.delete_admin))
async def delete_adm(message: types.Message, state: FSMContext):
    user_id = message.text
    
    if user_id.isdigit():
        await db.delete_admin(int(user_id))
        await message.answer(text=f"{user_id} <b>ID li foydalanuvchi adminlikdan olindi✅</b>", reply_markup=admin)
        await state.set_state(AdminState.main)
    else:
        await message.answer(text="<b>Iltimos, faqat raqamlardan foydalaning</b>")
        await state.set_state(AdminState.delete_admin)