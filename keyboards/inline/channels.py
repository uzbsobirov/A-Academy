from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def channels_func(lst, url):
    channels = InlineKeyboardMarkup(inline_keyboard=[])

    for number in range(1, lst + 1):
        button = InlineKeyboardButton(
            text=f"{number} - kanal",
            url=url[number - 1]
        )
        channels.inline_keyboard.append(button)

    check_button = InlineKeyboardButton(
        text="✅ Tasdiqlash",
        callback_data='check_subs'
    )

    channels.inline_keyboard.append([check_button])

    return channels
