from aiogram.types import Message
from aiogram.filters import BaseFilter

# from loader import db


class IsBotAdminFilter(BaseFilter):
    def __init__(self, get_admin_ids_func):
        self.get_admin_ids_func = get_admin_ids_func  # Pass the function to get admin IDs

    async def __call__(self, message: Message) -> bool:
        # Fetch the list of admin user_ids from the database
        admin_ids = await self.get_admin_ids_func()  # This function should return a list of admin IDs

        # Convert to int if needed (depends on how you store the IDs in the database)
        admin_ids_int = [int(id) for id in admin_ids]

        # Compare with the message sender's user_id
        return int(message.from_user.id) in admin_ids_int


# Example of an async function to get admin IDs from the database

