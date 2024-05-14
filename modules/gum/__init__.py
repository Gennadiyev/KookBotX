import asyncio
import json
import os
from datetime import datetime
import aiofiles
from typing import Union
import random
import shutil
from pathlib import Path
import string


class GameDataCorruptionError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class DuplicateRegistrationError(Exception):
    pass


class GameDataNotFoundError(Exception):
    pass


class BackupError(Exception):
    pass


def get_random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class UserManager:

    def __init__(self):
        self.data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.user_table = {}
        self.lock = asyncio.Lock()
        self.load_user_table()

    def load_user_table(self):
        user_table_path = self.data_dir / "user_table.json"
        if user_table_path.exists():
            self.user_table = json.loads(user_table_path.read_text())
        else:
            self.user_table = {}
            self.data_dir.mkdir(parents=True, exist_ok=True)
            user_table_path.write_text(json.dumps(self.user_table))

    async def register(self, user_id, game_id=None):
        async with self.lock:
            if user_id in self.user_table:
                raise DuplicateRegistrationError(
                    f"User {user_id} is already registered."
                )
            try:
                rsid = get_random_string()
                user_dir = self.data_dir / rsid
                os.makedirs(user_dir)
                self.user_table[user_id] = rsid

                meta = {
                    "kook_id": user_id,
                    "registration": {
                        "ts": datetime.now().timestamp(),
                        "time": datetime.now().isoformat(),
                        "from_game": game_id,
                    },
                }
                async with aiofiles.open(user_dir / "meta.json", "w") as f:
                    await f.write(json.dumps(meta))

                os.makedirs(user_dir / "backups")
                await self.save_user_table()
            except Exception as e:
                # Rollback if anything goes wrong
                if user_id in self.user_table:
                    del self.user_table[user_id]
                raise e

    async def unregister(self, user_id):
        async with self.lock:
            if user_id not in self.user_table:
                raise UserNotFoundError(f"User {user_id} not found.")
            try:
                del self.user_table[user_id]
                await self.save_user_table()
            except Exception as e:
                raise e

    async def save_user_table(self):
        async with aiofiles.open(self.data_dir / "user_table.json", "w") as f:
            await f.write(json.dumps(self.user_table))

    async def has_user(self, user_id):
        return user_id in self.user_table

    async def get_data_for_game(self, user_id, game_id):
        if user_id not in self.user_table:
            raise UserNotFoundError(f"User {user_id} not found.")

        user_dir = self.data_dir / self.user_table[user_id]
        game_data_path = user_dir / f"{game_id}.dat"

        if not game_data_path.exists():
            raise GameDataNotFoundError(
                f"Data for game {game_id} not found for user {user_id}."
            )

        try:
            async with aiofiles.open(game_data_path, "rb") as f:
                return await f.read()
        except Exception as e:
            raise GameDataCorruptionError(
                f"Data corruption for game {game_id} of user {user_id}, failed to read {game_data_path}."
            ) from e

    async def has_data_for_game(self, user_id, game_id):
        if user_id not in self.user_table:
            return False

        user_dir = self.data_dir / self.user_table[user_id]
        game_data_path = user_dir / f"{game_id}.dat"
        return game_data_path.exists()

    async def set_data_for_game(
        self, user_id, game_id, data, backup=False
    ):
        async with self.lock:
            if user_id not in self.user_table:
                raise UserNotFoundError(f"User {user_id} not found.")
            
            if isinstance(data, str):
                data = data.encode("utf-8")
                logger.warning("Writing string to game data is not recommended, please use bytes.")

            user_dir = self.data_dir / self.user_table[user_id]
            game_data_path = user_dir / f"{game_id}.dat"
            backup_path = (
                user_dir / "backups" / f"{game_id}.dat.{datetime.now().timestamp()}.bak"
            )

            try:
                if backup and game_data_path.exists():
                    shutil.copy(game_data_path, backup_path)
                async with aiofiles.open(game_data_path, "wb") as f:
                    await f.write(data)
            except Exception as e:
                if backup:
                    raise BackupError(
                        f"Failed to backup data for game {game_id} of user {user_id}."
                    ) from e
                raise GameDataCorruptionError(
                    f"Failed to set data for game {game_id} of user {user_id}, failed to write {game_data_path}."
                ) from e

    async def delete_data_for_game(self, user_id, game_id):
        async with self.lock:
            if user_id not in self.user_table:
                raise UserNotFoundError(f"User {user_id} not found.")

            user_dir = self.data_dir / self.user_table[user_id]
            game_data_path = user_dir / f"{game_id}.dat"
            deleted_backup_path = (
                user_dir / "backups" / f"{game_id}.dat.{datetime.now().timestamp()}.del"
            )
        if not game_data_path.exists():
            raise GameDataNotFoundError(
                f"Data for game {game_id} not found for user {user_id}."
            )
        try:
            shutil.move(game_data_path, deleted_backup_path)
        except Exception as e:
            raise e

    async def meta_get(self, user_id):
        if user_id not in self.user_table:
            raise UserNotFoundError(f"User {user_id} not found.")

        user_dir = self.data_dir / self.user_table[user_id]
        meta_path = user_dir / "meta.json"

        try:
            async with aiofiles.open(meta_path, "r") as f:
                return json.loads(await f.read())
        except Exception as e:
            raise e

    async def meta_set(self, user_id, meta_key, meta_value):
        async with self.lock:
            if user_id not in self.user_table:
                raise UserNotFoundError(f"User {user_id} not found.")

            user_dir = self.data_dir / self.user_table[user_id]
            meta_path = user_dir / "meta.json"
            backup_path = (
                user_dir / "backups" / f"meta.json.{datetime.now().timestamp()}.bak"
            )

            try:
                # Backup current meta
                shutil.copy(meta_path, backup_path)

                # Read, update, and write back meta
                async with aiofiles.open(meta_path, "r+") as f:
                    meta = json.loads(await f.read())
                    meta[meta_key] = meta_value
                    await f.seek(0)
                    await f.write(json.dumps(meta))
                    await f.truncate()
            except Exception as e:
                raise e

    async def dump_user_table(self):
        return self.user_table


gum = UserManager()
