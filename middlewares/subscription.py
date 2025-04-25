from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message

from keyboards.inline.channels import channels_func


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        channels = [
            -1001546336057,
            "@qiyqiriquzz"
        ]
        channels_urls = []

        channel_statuses = []
        for channel in channels:
            status = await event.bot.get_chat_member(
                chat_id=channel,
                user_id=event.from_user.id
            )
            url = await event.bot.get_chat(channel)
            channel_statuses.append(status.status)
            channels_urls.append(url.invite_link)

        if 'left' in channel_statuses:
            text = "<b>❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.</b>"

            await event.answer(
                text=text,
                reply_markup=channels_func(len(channels), url=channels_urls)
            )
        else:
            return await handler(event, data)