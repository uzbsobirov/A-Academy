from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from keyboards.inline.panel import test_buttons
from states.panel import AdminState

router = Router()


@router.callback_query(StateFilter(AdminState.main), F.data == "create_test")
async def settings_test(call: types.CallbackQuery, state: FSMContext):
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
    await call.message.edit_text(text="<b>Har bir test uchun qancha ball bermoqchi ekanligingizni kiriting👇\n\n"
                                      "Masalan: 2</b>")
    await state.set_state(AdminState.ball)


@router.message(StateFilter(AdminState.ball))
async def get_bal(message: types.Message, state: FSMContext):
    ball = message.text

    if ball.isdigit():
        print("Yes")
    else:
        print("no")

