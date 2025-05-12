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
                text="👥 Adminlar",
                callback_data="admins_list"
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


required1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Kanal qo'shish",
                callback_data="add_channel"
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


required2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Kanal qo'shish",
                callback_data="add_channel"
            ),
            InlineKeyboardButton(
                text="➖ Kanal o'chirish",
                callback_data="delete_channel"
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


settings_admins = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Admin qo'shish",
                callback_data="add_admin"
            ),
            InlineKeyboardButton(
                text="➖ Adminlikdan olish",
                callback_data="delete_admin"
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


test_buttons1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📈 Test bali",
                callback_data="test_ball"
            ),
            InlineKeyboardButton(
                text="✅ To'g'ri javoblar soni",
                callback_data="real_answers_number"

            )
        ],
        [
            InlineKeyboardButton(
                text="✅ To'g'ri javoblarni ko'rsatish",
                callback_data="real_answer_show"
            ),
            InlineKeyboardButton(
                text="✅ Xato javoblarni ko'rsatish",
                callback_data="wrong_answer_show"
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


def test_buttons(settings):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"📈 Test bali",
                callback_data=f"test_ball"
            ),
            InlineKeyboardButton(
                text=f"✅ To'g'ri javoblar soni" if settings[0]['num_answers'] == 'on' else "❌ To'g'ri javoblar soni",
                callback_data=f"toggle:num_answers:{settings[0]['num_answers']}"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"✅ To'g'ri javoblarni ko'rsatish" if settings[0]['real_answers'] == 'on' else "❌ To'g'ri javoblarni ko'rsatish",
                callback_data=f"toggle:real_answers:{settings[0]['real_answers']}"
            ),
            InlineKeyboardButton(
                text=f"✅ Xato javoblarni ko'rsatish" if settings[0]['wrong_answers'] == 'on' else "❌ Xato javoblarni ko'rsatish",
                callback_data=f"toggle:wrong_answers:{settings[0]['wrong_answers']}"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"⛔️ Testni tugatish",
                callback_data=f"cancel_test"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back"
            )
        ]
    ])
    return keyboard



















