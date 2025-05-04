import re
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fractions import Fraction

from loader import db
from states.panel import AdminState

router = Router()


def normalize_answer(ans: str) -> str:
    ans = ans.strip().lower()
    if re.match(r"^\d+/\d+$", ans):  # fraction
        return str(round(float(Fraction(ans)), 4))
    try:
        return str(round(float(ans), 4))  # float or int
    except ValueError:
        return ans  # letter answers like 'a', 'b', etc.


# Handler for messages starting with "digit*"
@router.message(F.text.regexp(r"^\d+\*"))
async def handle_test_submission(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if '*' not in text:
        await message.answer("❌ Xabar formati noto'g'ri. Masalan: 44*a,b,c")
        return

    test_id_str, answers_str = text.split('*', 1)

    try:
        test_id = int(test_id_str)
    except ValueError:
        await message.answer("❌ Test ID noto‘g‘ri.")
        return

    user_id = message.from_user.id

    # Check if user already submitted this test
    already_sent = await db.select_participants(code=test_id, user_id=user_id)

    get_answers = await db.select_answers(code=test_id)
    correct_answers = [normalize_answer(a) for a in get_answers.split(',')]
    user_answers = [normalize_answer(a) for a in answers_str.split(',')]
    user_answer_count = len(user_answers)
    admin_answer_count = len(correct_answers)

    if already_sent:
        await message.answer("⚠️ Siz ushbu testga allaqachon javob yuborgansiz.")
        return

    else:
        if not get_answers:
            await message.answer("❌ Bunday test mavjud emas.")
            return

        if user_answer_count != admin_answer_count:
            await message.answer(
                f"⚠️ Siz {user_answer_count} ta javob yubordingiz, ammo bu testda {admin_answer_count} ta savol mavjud.\n"
                "Natija noto‘g‘ri bo‘lishi mumkin."
            )

        else:
            await db.add_participants(code=test_id, user_id=user_id)
            score = sum(1 for i in range(min(len(correct_answers), len(user_answers)))
                        if correct_answers[i] == user_answers[i])
            print(score)
            print(correct_answers, len(correct_answers))
            print(user_answers, len(user_answers))

            percent = round(score / len(correct_answers) * 100, 2)

            await message.answer(
                f"✅ Test {test_id} yakunlandi.\n"
                f"To‘g‘ri javoblar soni: {score}/{len(correct_answers)}\n"
                f"Foiz: {percent}%"
            )




    # Save result
    # await db.execute(
    #     "INSERT INTO test_submissions (user_id, test_id, answers, score) VALUES ($1, $2, $3, $4)",
    #     user_id, test_id, answers_str, percent
    # )



# @router.callback_query(F.data == "testing")
# async def check_test_submission(call: types.CallbackQuery, state: FSMContext):
#     await call.message.edit_text(text="<b>Iltimos javoblarni kiriting...\n\nMasalan: 44*a,b,c,1/2,-0.5</b>")
#     await state.set_state(AdminState.get_answers)
#
#
# @router.message(StateFilter(AdminState.get_answers))
# async def get_answer_keys(message: types.Message, state: FSMContext):
#     # text = message.text.strip()
#     print(message.text)
#     print(123)

    # if bool(re.match(r"^\d+\*", text.strip())):
    # if '*' not in text:
    #     await message.answer("Xatolik: format noto'g'ri. Masalan: 44*a,b,c,...")
    #     return
    #
    # test_id_str, answers_str = text.split('*', 1)
    #
    # try:
    #     test_id = int(test_id_str)
    # except ValueError:
    #     await message.answer("Xatolik: test ID raqam bo'lishi kerak.")
    #     return
    #
    # user_answers = [a.strip() for a in answers_str.split(',') if a.strip()]
    #
    # # Get correct answers from DB
    # correct_answers = await db.select_test(test_id)
    #
    # if correct_answers is None:
    #     await message.answer(f"Test ID {test_id} topilmadi.")
    #     return
    #
    # # Compare answers
    # score = 0
    # total = min(len(user_answers), len(correct_answers))
    # for i in range(total):
    #     if str(user_answers[i]).lower() == str(correct_answers[i]).lower():
    #         score += 1
    #
    # percent = round((score / len(correct_answers)) * 100, 2)
    #
    # # Save result
    # await db.save_submission(
    #     user_id=message.from_user.id,
    #     test_id=test_id,
    #     answers=user_answers,
    #     score=percent
    # )
    #
    # await message.answer(f"✅ Test {test_id} tekshirildi.\nTo'g'ri javoblar: {score}/{len(correct_answers)}\nFoiz: {percent}%")
    #
    # # else:
    # #     print("ishlamadi")
