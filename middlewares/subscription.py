from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message
import logging

from keyboards.inline.channels import channels_func
from loader import db

logger = logging.getLogger(__name__)


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # 🔁 Fetch channel list from DB
        db_channels = await db.select_all_sponsors()
        if not db_channels:
            logger.warning("No channels found in the database.")
            return await handler(event, data)

        unsubscribed_urls = []
        unsubscribed_count = 0

        for row in db_channels:
            channel_id = row["chat_id"]
            member = await event.bot.get_chat_member(
                chat_id=channel_id,
                user_id=event.from_user.id
            )

            if member.status == "left":
                chat = await event.bot.get_chat(channel_id)
                unsubscribed_urls.append(chat.invite_link)
                unsubscribed_count += 1

        if unsubscribed_count > 0:
            text = "<b>❌ Kechirasiz, botdan foydalanishdan oldin quyidagi kanallarga a'zo bo'lishingiz kerak.</b>"

            await event.answer(
                text=text,
                reply_markup=channels_func(unsubscribed_count, url=unsubscribed_urls)
            )
        else:
            return await handler(event, data)