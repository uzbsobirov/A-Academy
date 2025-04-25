from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NULL,
        username varchar(255) NULL,
        user_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_sponsors(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Sponsors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NULL,
        username varchar(255) NULL,
        chat_id BIGINT NOT NULL UNIQUE,
        invite_link VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, user_id):
        sql = "INSERT INTO users (full_name, username, user_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, user_id, fetchrow=True)

    async def add_sponsor(self, name, username, chat_id, invite_link):
        sql = "INSERT INTO Sponsors (name, username, chat_id, invite_link) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, name, username, chat_id, invite_link, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_sponsors(self):
        sql = "SELECT * FROM Sponsors"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def select_one_user(self, user_id):
        sql = "SELECT * FROM Users WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def update_user_name(self, full_name, user_id):
        sql = "UPDATE Users SET full_name=$1 WHERE user_id=$2"
        return await self.execute(sql, full_name, user_id, execute=True)

    async def delete_sponsor(self, id: int):
        query = "DELETE FROM Sponsors WHERE id=$1"
        await self.execute(query, id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
