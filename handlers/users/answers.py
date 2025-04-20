from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode


from keyboards.inline.backs import back
from states.simple import HowAnswer

router = Router()


@router.callback_query(F.data == "how_answer")
async def how_to_answer(call: types.CallbackQuery, state: FSMContext):
    text = """*❗️Testga javob berish

✅Test kodini kiritib \* \(yulduzcha\) belgisini qo'yasiz va barcha kalitlarni kiritasiz\.

✍️Misol uchun\:
> 123\*abcdab\.\.\. yoki 
> 123\*a,b,c,d,a,b\.\.\.
⁉️Testga faqat bir marta javob berish mumkin\.

✅Katta\(A\) va kichik\(a\) harflar bir xil hisoblanadi\.*"""
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=back)
    await state.set_state(HowAnswer.about)