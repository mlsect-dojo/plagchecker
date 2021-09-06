import aiosqlite
import pathlib

db_path = f'{pathlib.Path(__file__).parent.resolve()}/../plagchecker.db'

class SQLite():

    @staticmethod
    async def insert_lab(filename):
        async with aiosqlite.connect(db_path) as db:
            await db.execute(f"INSERT INTO labs (path) VALUES ('{filename}');")
            await db.commit()
            async with db.execute(f"SELECT id FROM labs WHERE path = '{filename}';") as cursor:
                row = await cursor.fetchone()

        return row[0]

    @staticmethod
    async def delete_lab(lab_id):
        async with aiosqlite.connect(db_path) as db:
            async with db.execute(f"SELECT path FROM labs WHERE id = {lab_id};") as cursor:
                row = await cursor.fetchone()
            await db.execute(f"DELETE FROM labs WHERE id = {lab_id};")
            await db.commit()

        if row:
            return row[0]
        else:
            return None
            