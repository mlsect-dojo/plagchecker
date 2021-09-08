from fastapi import FastAPI, File, UploadFile
import uuid
import pathlib
import aiofiles
import aiofiles.os
import uvicorn

from api.utils.db import SQLiteConnector

server = FastAPI()

@server.put('/lab')
async def save_lab(archive: UploadFile = File(...)):
    filename = f'{uuid.uuid4()}.zip'
    data = archive.file.read()
    async with aiofiles.open(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{filename}', 'wb') as file:
        await file.write(data)

    lab_id = await SQLiteConnector.insert_lab(f'{filename}')

    return {'id': lab_id}

@server.delete('/lab')
async def delete_lab(lab_id: int):
    path = await SQLiteConnector.delete_lab(lab_id)

    if path:
        await aiofiles.os.remove(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{path}')

    return {'status': 'OK'}

@server.post('/score/all')
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

@server.post('/score/levenstein')
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
    uvicorn.run('server:server', port = 5050, reload = True)
    