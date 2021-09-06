import aiosqlite
from fastapi import FastAPI, File, UploadFile
import uuid
import pathlib
import aiofiles
import aiofiles.os
import uvicorn

api = FastAPI()

@api.put('/lab')
async def save_lab(archive: UploadFile = File(...)):
    filename = uuid.uuid4()
    data = archive.file.read()
    async with aiofiles.open(f'{pathlib.Path(__file__).parent.resolve()}/labs/{filename}.zip', 'wb') as file:
        await file.write(data)

    async with aiosqlite.connect(f'{pathlib.Path(__file__).parent.resolve()}/plagchecker.db') as db:
        await db.execute(f"INSERT INTO labs (path) VALUES ('{f'{filename}.zip'}')")
        await db.commit()
        async with db.execute(f"SELECT id FROM labs WHERE path = '{f'{filename}.zip'}'") as cursor:
            row = await cursor.fetchone()

    return {'id': row[0]}

@api.delete('/lab')
async def delete_lab(lab_id: int):
    async with aiosqlite.connect(f'{pathlib.Path(__file__).parent.resolve()}/plagchecker.db') as db:
        async with db.execute(f"SELECT path FROM labs WHERE id = {lab_id};") as cursor:
            row = await cursor.fetchone()
        await db.execute(f"DELETE FROM labs WHERE id = {lab_id};")
        await db.commit()
    
    if row:
        await aiofiles.os.remove(f'{pathlib.Path(__file__).parent.resolve()}/labs/' + row[0])

    return {'status': 'OK'}

@api.post('/score/all')
async def lab_score_all(archive: UploadFile = File(...)):
    #do checks
    return {
        'similars': [
            {
                'algorithm': 'string',
                'top': [
                    {
                        'id': 3,
                        'score': 1
                    }
                ]
            }
        ]
    }

@api.post('/score/levenstein')
async def lab_score_levenstein(archive: UploadFile = File(...)):
    #do levenstein check
    return {
        'similars': [
            {
                'id': 0,
                'score': 2
            }
        ]
    }

if __name__ == '__main__':
    uvicorn.run('api:api', port = 5050, reload = True)