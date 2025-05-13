import re
from aiogram import Router, F, types
import pandas as pd
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from tabulate import tabulate

from data.config import ADMINS
from filters import IsBotAdminFilter
from loader import db, bot
from states import AdminState

router = Router()


async def send_detailed_result(message, test_id, user_answers, correct_answers, settings):
    user_id = message.from_user.id
    user_info = await db.select_one_user(user_id)
    user_mention = f"<a href='tg://user?id={user_info['user_id']}'>{user_info[1]}</a>"

    result_text = [f"<b>{user_mention} ning natijasi",
                   f"📌Test kodi: {test_id}",
                   f"📋Savollar soni: {len(correct_answers)} ta\n",
                   "Natijalari:</b>"]

    score = 0
    wrong_count = 0
    for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers), 1):
        is_correct = user_ans == correct_ans
        mark = "✅" if is_correct else "❌"
        point = "1 ball" if is_correct else "0 ball"
        line = f"<b>{i}. {user_ans.upper()} {mark}</b>"

        if not is_correct and settings[0]['real_answers'] == 'on':
            line += f"<b> | To'g'ri javob: {correct_ans.upper()}</b>"

        line += f"\t{point}"
        result_text.append(line)

        if is_correct:
            score += 1
        else:
            wrong_count += 1

    percent = round(score / len(correct_answers) * 100, 2)
    result_text.append("")
    result_text.append(f"<b>📊 Jami: {score} ball</b>")

    if settings[0]['num_answers'] == 'on':
        result_text.append(f"<b>✅ To'g'ri javoblar soni: {score}</b>")

    if settings[0]['wrong_answers'] == 'on':
        result_text.append(f"<b>❌ Xato javoblar soni: {wrong_count}</b>")

    result_text.append(f"<b>☑️ Natija: {percent} %</b>")

    await message.answer("\n".join(result_text))

    await db.add_participants(code=test_id, user_id=user_id, score=score)

#######


@router.callback_query(StateFilter(AdminState.test_set), F.data == "cancel_test")
async def get_final(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Bekor qilmoqchi bo'lgan testingizni kodini yuboring</b>")
    await state.set_state(AdminState.cancel)


@router.message(StateFilter(AdminState.cancel))
async def cancel_test_id(message: types.Message, state: FSMContext):
    text = message.text
    print(text)

    if text.isdigit():
        results = await db.select_participantss(code=int(text))
        print(results)

        if not results:
            await message.answer(f"❌ {int(text)}-sonli testga hech kim qatnashmagan yoki test mavjud emas.")
            return

            # Malumotlarni DataFrame ga o'tkazish
        df = pd.DataFrame(results, columns=["test_id", "code", "user_id", "score"])

        # Ism-familiyalarni bazadan olish (faraz qilamiz sizda user jadvali bor)
        names = []
        for user_id in df["user_id"]:
            select_user = await db.select_one_user(user_id=user_id)
            names.append(select_user['full_name'])
        #     user = await db.get_user(user_id)  # bu user['full_name'] deb olish mumkin bo'lgan funksiya bo'lishi kerak
        #     names.append(user["full_name"] if user else "Noma'lum foydalanuvchi")

        df["name"] = names
        df["percentage"] = df["score"].astype(float) / 44 * 100  # 44 - savollar soni
        df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

        # Natijani tuzish
        result_text = f"📊 <b>{int(text)}-sonli test natijalari:</b>\n\n"
        for idx, row in df.iterrows():
            user_link = f'<a href="tg://user?id={row["user_id"]}">{row["name"]}</a>'
            result_text += (
                f"{idx + 1}. {user_link} - {row['score']} ta - "
                f"{round(row['percentage'], 2)}%\n"
            )

        await message.answer(result_text)
        await state.clear()
        # df = pd.DataFrame(results, columns=["test_id", "code", "user_id", "score"])
        # df = df.sort_values(by="score", ascending=False)  # bal bo‘yicha kamayish tartibi
        # df.index = range(1, len(df) + 1)  # T/r raqamlari
        #
        # table_text = tabulate(df, headers=["T/r", "Ism", "Ball", "Foiz", "Vaqt"], tablefmt="grid", showindex=True)
        #
        # for admin_id in ADMINS:
        #     await bot.send_message(
        #         chat_id=admin_id,
        #         text=f"📊 *{int(text)}-sonli test yakunlandi!*\n\n```{table_text}```",
        #         parse_mode="Markdown"
        #     )


    else:
        await message.answer(text="<b>Iltimos faqat raqamlardan foydalaning</b>")
        await state.set_state(AdminState.cancel)



