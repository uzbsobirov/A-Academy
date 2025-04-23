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
                text="📝 Test ishlash",
                callback_data="testing"
            )
        ]
    ]
)



