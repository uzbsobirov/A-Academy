import re
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from keyboards.inline.panel import test_buttons
from loader import db
from states.panel import AdminState

router = Router()


@router.callback_query(StateFilter(AdminState.main), F.data == "create_test")
async def settings_test(call: types.CallbackQuery, state: FSMContext):
    all_settings = await db.select_all_settings()
    if len(all_settings) == 0:
        await db.add_settings(ball=1, real_answers='on', num_answers='on', wrong_answers='on')
    else:
        pass

    text = """*✅Test nomini kiritib \+ \(plus\) belgisini qo'yasiz\. Va barcha kalitni kiritasiz\.

✍️Misol uchun\:
> Matematika\+abcdab\.\.\. yoki 
> Matematika\+a\,b\,c\,d\,a\,b\.\.\.
⁉️Testga faqat bir marta javob berish mumkin\.

✅Katta\(A\) va kichik\(a\) harflar bir xil hisoblanadi\.

🗄Test natijalari 30 kun saqlanadi\!*"""
    await call.message.delete()
    await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=test_buttons(all_settings))
    await state.set_state(AdminState.test_set)


@router.callback_query(StateFilter(AdminState.test_set), F.data == "test_ball")
async def test_balls(call: types.CallbackQuery, state: FSMContext):
    all_settings = await db.select_all_settings()
    ball = all_settings[0]['ball']
    await call.message.edit_text(text="<b>Har bir test uchun qancha ball bermoqchi ekanligingizni kiriting👇\n\n"
                                      f"Masalan: 2\n\nHozirgi ball: {ball}</b>")
    await state.set_state(AdminState.ball)


@router.message(StateFilter(AdminState.ball))
async def get_bal(message: types.Message, state: FSMContext):
    all_settings = await db.select_all_settings()

    ball = message.text

    if ball.isdigit():
        await db.update_settings(ball=int(ball), id=1)
        await message.answer(text=f"<b>Har bir test uchun ball {ball} ga o'zgardi✅</b>")
        text = """*✅Test nomini kiritib \+ \(plus\) belgisini qo'yasiz\. Va barcha kalitni kiritasiz\.

✍️Misol uchun\:
> Matematika\+abcdab\.\.\. yoki 
> Matematika\+a\,b\,c\,d\,a\,b\.\.\.
⁉️Testga faqat bir marta javob berish mumkin\.

✅Katta\(A\) va kichik\(a\) harflar bir xil hisoblanadi\.

🗄Test natijalari 30 kun saqlanadi\!*"""
        # await message.delete()
        await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=test_buttons(all_settings))
        await state.set_state(AdminState.test_set)

    else:
        await message.answer(text="<b>Iltimos faqat sonlardan foydalaning❗️</b>")
        await state.set_state(AdminState.ball)


# ///// RIGHT ANSWERS NUMBER /////
@router.callback_query(StateFilter(AdminState.test_set), F.data.startswith("toggle:"))
async def right_answers(call: types.CallbackQuery, state: FSMContext):
    all_settings = await db.select_all_settings()

    _, setting_name, current_value = call.data.split(":")
    id = all_settings[0]['id']

    # Toggle value
    new_value = "off" if current_value == "on" else "on"

    # Update DB
    if new_value:
        await db.update_settings_answer_num(id=id, new_value=new_value, column_name=setting_name)

    get_new = await db.select_all_settings()

    await call.message.delete()
    text = """*✅Test nomini kiritib \+ \(plus\) belgisini qo'yasiz\. Va barcha kalitni kiritasiz\.

✍️Misol uchun\:
> Matematika\+abcdab\.\.\. yoki 
> Matematika\+a\,b\,c\,d\,a\,b\.\.\.
⁉️Testga faqat bir marta javob berish mumkin\.

✅Katta\(A\) va kichik\(a\) harflar bir xil hisoblanadi\.

🗄Test natijalari 30 kun saqlanadi\!*"""
    await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=test_buttons(get_new))
    await state.set_state(AdminState.get_code)


@router.message()
async def get_test_code(message: types.Message, state: FSMContext):
    text = message.text.strip()
    name, answers = message.text.split('*')

    if re.match(r"^[a-zA-Z]", text):
        correct_answers = [a.strip().lower() for a in text.split(',') if a.strip()]
        await db.add_test(name=name, answers=answers)
        await message.answer(f"✅ Yangi test yaratildi: Nomi {name}")

















