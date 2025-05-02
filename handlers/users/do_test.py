import re
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from loader import db
from states.panel import AdminState

router = Router()


@router.message()
async def check_test_submission(message: types.Message, state: FSMContext):
    text = message.text.strip()
    print(text)

    # if bool(re.match(r"^\d+\*", text.strip())):
    if '*' not in text:
        await message.answer("Xatolik: format noto'g'ri. Masalan: 44*a,b,c,...")
        return

    test_id_str, answers_str = text.split('*', 1)

    try:
        test_id = int(test_id_str)
    except ValueError:
        await message.answer("Xatolik: test ID raqam bo'lishi kerak.")
        return

    user_answers = [a.strip() for a in answers_str.split(',') if a.strip()]

    # Get correct answers from DB
    correct_answers = await db.select_test(test_id)

    if correct_answers is None:
        await message.answer(f"Test ID {test_id} topilmadi.")
        return

    # Compare answers
    score = 0
    total = min(len(user_answers), len(correct_answers))
    for i in range(total):
        if str(user_answers[i]).lower() == str(correct_answers[i]).lower():
            score += 1

    percent = round((score / len(correct_answers)) * 100, 2)

    # Save result
    await db.save_submission(
        user_id=message.from_user.id,
        test_id=test_id,
        answers=user_answers,
        score=percent
    )

    await message.answer(f"✅ Test {test_id} tekshirildi.\nTo'g'ri javoblar: {score}/{len(correct_answers)}\nFoiz: {percent}%")

    # else:
    #     print("ishlamadi")
