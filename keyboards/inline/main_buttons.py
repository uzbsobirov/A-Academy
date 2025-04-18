from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔠 Testga qanday javob beriladi?",
                callback_data="how_answer"
        )
        ],
        [
            InlineKeyboardButton(
                text="🆕 Yangi test qanday yaratiladi?",
                callback_data="new_test"
        )
        ],
        [
            InlineKeyboardButton(
                text="Botda test ishlash va yaratish(+video)",
                callback_data="video_exp"
        )
        ]
    ]
)

main2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🆕 Yangi test qanday yaratiladi?",
                callback_data="new_test"
        )
        ],
        [
            InlineKeyboardButton(
                text="Botda test ishlash va yaratish(+video)",
                callback_data="video_exp"
        )
        ]
    ]
)