import pathlib

import aiosqlite

class SQLiteConnector():

    def __init__(self) -> None:
        self.db_path = f'{pathlib.Path(__file__).parent.parent.resolve()}/plagchecker.db'

    async def insert_lab(self, filename: str, user_id: int, ext: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"INSERT INTO labs (path, user_id, extension) VALUES ('{filename}', {user_id}, '{ext}');")
            await db.commit()
            async with db.execute(f"SELECT id FROM labs WHERE path = '{filename}';") as cursor:
                row = await cursor.fetchone()

        return row[0]

    async def delete_lab(self, lab_id: int) -> str:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT path FROM labs WHERE id = {lab_id};") as cursor:
                row = await cursor.fetchone()
            await db.execute(f"DELETE FROM labs WHERE id = {lab_id};")
            await db.commit()

        if row:
            return row[0]
        else:
            return None

    async def get_lab_info_filename(self, filename: str) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT * FROM labs WHERE path = '{filename}';") as cursor:
                row = await cursor.fetchone()
        if row:
            return {'lab_id': row[0], 'filename': row[1], 'user_id': row[2], 'ext': row[3]}
        else:
            return None

    async def get_lab_info_id(self, lab_id: int) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT * FROM labs WHERE id = '{lab_id}';") as cursor:
                row = await cursor.fetchone()
        if row:
            return {'lab_id': row[0], 'filename': row[1], 'user_id': row[2], 'ext': row[3]}
        else:
            return None
