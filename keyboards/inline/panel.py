from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔐 Majburiy obuna",
                callback_data="majburiy"
        ),
            InlineKeyboardButton(
                text="📊 Statistika",
                callback_data="statistic"
        )
        ],
        [
            InlineKeyboardButton(
                text="📝 Test yaratish",
                callback_data="create_test"
            ),
            InlineKeyboardButton(
                text="📨 Reklama yuborish",
                callback_data="send_ads"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back"
            )
        ]
    ]
)