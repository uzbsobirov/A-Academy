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
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=test_buttons)
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
        await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=test_buttons)
        await state.set_state(AdminState.test_set)

    else:
        await message.answer(text="<b>Iltimos faqat sonlardan foydalaning❗️</b>")
        await state.set_state(AdminState.ball)


# ///// RIGHT ANSWERS NUMBER /////
@router.callback_query(StateFilter(AdminState.test_set), F.data == "real_answers_number")
async def right_answers(call: types.CallbackQuery, state: FSMContext):
    all_settings = await db.select_all_settings()
    right_answers_number = all_settings[0]['num_answers']

    if right_answers_number == 'on':
        await db.update_settings_answer_num(num_answers='off', id=1)

    else:
        await db.update_settings_answer_num(num_answers='on', id=1)
















