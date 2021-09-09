import pathlib
import uuid

import aiofiles
import aiofiles.os
import uvicorn
from fastapi import FastAPI, File, UploadFile

from api.utils.checks import Checks
from api.utils.sqliteconnector import SQLiteConnector

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

@server.get('/score/all')
async def lab_score_all(lab_id: int, limit: int = None):
    result = await Checks.check_all(lab_id, limit)
    return result

@server.get('/score/levenshtein')
async def lab_score_levenshtein(lab_id: int, limit: int = None):
    similars = await Checks.levenshtein_check(False, lab_id, limit)
    return similars

if __name__ == '__main__':
    uvicorn.run('server:server', port = 5050, reload = True)
    