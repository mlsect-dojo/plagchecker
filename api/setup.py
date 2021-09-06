import aiosqlite
import asyncio
import pathlib

async def main():
    async with aiosqlite.connect(f'{pathlib.Path(__file__).parent.resolve()}/plagchecker.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS labs (
            id INTEGER NOT NULL,
            path TEXT,
            PRIMARY KEY (id AUTOINCREMENT)
        );""")

asyncio.run(main())