import re
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fractions import Fraction

from loader import db
from states.panel import AdminState
from utils.extra_datas import make_title

router = Router()


def normalize_answer(ans: str) -> str:
    ans = ans.strip().lower()
    if re.match(r"^\d+/\d+$", ans):  # fraction
        return str(round(float(Fraction(ans)), 4))
    try:
        return str(round(float(ans), 4))  # float or int
    except ValueError:
        return ans  # letter answers like 'a', 'b', etc.


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

    # Check if test exists
    get_answers = await db.select_answers(code=test_id)
    if not get_answers:
        await message.answer("❌ Bunday test mavjud emas.")
        return

    # Normalize answers
    correct_answers = [normalize_answer(a) for a in get_answers.split(',')]
    user_answers = [normalize_answer(a) for a in answers_str.split(',')]

    user_answer_count = len(user_answers)
    correct_answer_count = len(correct_answers)

    # Check if already submitted
    already_sent = await db.select_participants(code=test_id, user_id=user_id)
    if already_sent:
        await message.answer("⚠️ Siz ushbu testga allaqachon javob yuborgansiz.")
        return

    # Check if answers are complete
    if user_answer_count != correct_answer_count:
        await message.answer(
            f"❌ Siz {user_answer_count} ta javob yubordingiz, ammo bu testda {correct_answer_count} ta savol bor.\n"
            "Iltimos, to‘liq javob yuboring."
        )
        return

    # Save the participant
    await db.add_participants(code=test_id, user_id=user_id)

    # Calculate score
    score = sum(1 for i in range(correct_answer_count) if correct_answers[i] == user_answers[i])
    percent = round(score / correct_answer_count * 100, 2)

    select_user = await db.select_one_user(user_id=user_id)
    user_mention = f"[{make_title(select_user[0]['name'])}](tg://user?id={user_id})"
    final_text = f"""<b>{user_mention} ning natijasi

> 📌Test kodi: {test_id}
> 📋Savollar soni: {correct_answer_count} ta

Natijalari:
"""


    await message.answer(
        f"✅ Test {test_id} yakunlandi.\n"
        f"To‘g‘ri javoblar soni: {score}/{correct_answer_count}\n"
        f"Foiz: {percent}%"
    )

    print("User answers:", user_answers)
    print("Correct answers:", correct_answers)
    print("User answer count:", len(user_answers))
    print("Correct answer count:", len(correct_answers))

