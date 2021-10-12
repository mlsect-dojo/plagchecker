import aiosqlite
import asyncio
import pathlib

async def main():
    async with aiosqlite.connect(f'{pathlib.Path(__file__).parent.resolve()}/plagchecker.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS labs (
            id INTEGER NOT NULL,
            path TEXT,
            user_id INTEGER NOT NULL,
            extension STRING NOT NULL,
            PRIMARY KEY (id AUTOINCREMENT)
        );""")
        await db.execute("""CREATE TABLE IF NOT EXISTS results (
            id INTEGER NOT NULL,
            compared INTEGER NOT NULL,
            compared_to INTEGER NOT NULL,
            algorithm TEXT NOT NULL,
            score REAL,
            PRIMARY KEY (id AUTOINCREMENT)
            FOREIGN KEY (compared) REFERENCES labs (id),
            FOREIGN KEY (compared_to) REFERENCES labs(id)
        );""")

asyncio.run(main())
