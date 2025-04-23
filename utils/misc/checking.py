from typing import Union
from loader import bot


async def check_is_subs(user_id, chat_id: Union[str, int]):
    member = await bot.get_chat_member(user_id=user_id, chat_id=chat_id)
    return member.is_member()

async def check_is_admin(chat_id: Union[str, int]):
    member = await bot.get_chat_administrators(chat_id=chat_id)
    return member