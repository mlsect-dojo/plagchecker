import aiosqlite
import pathlib

class SQLiteConnector():
    db_path = f'{pathlib.Path(__file__).parent.parent.resolve()}/plagchecker.db'

    @classmethod
    async def insert_lab(cls, filename: str) -> int:
        async with aiosqlite.connect(cls.db_path) as db:
            await db.execute(f"INSERT INTO labs (path) VALUES ('{filename}');")
            await db.commit()
            async with db.execute(f"SELECT id FROM labs WHERE path = '{filename}';") as cursor:
                row = await cursor.fetchone()

        return row[0]

    @classmethod
    async def delete_lab(cls, lab_id: int) -> str:
        async with aiosqlite.connect(cls.db_path) as db:
            async with db.execute(f"SELECT path FROM labs WHERE id = {lab_id};") as cursor:
                row = await cursor.fetchone()
            await db.execute(f"DELETE FROM labs WHERE id = {lab_id};")
            await db.commit()

        if row:
            return row[0]
        else:
            return None
