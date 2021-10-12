import uvicorn
from fastapi import FastAPI, File, UploadFile

from api.utils.lab_scoring_handler import LabScoringHandler

server = FastAPI()
handler = LabScoringHandler()

@server.put('/lab')
async def save_lab(user_id: int, ext: str, archive: UploadFile = File(...)):
    lab_id = await handler.save_lab(user_id, ext, archive)
    return {'id': lab_id}

@server.delete('/lab')
async def delete_lab(lab_id: int):
    await handler.delete_lab(lab_id)
    return {'status': 'OK'}

@server.get('/score/all')
async def lab_score_all(lab_id: int, limit: int = None):
    result = await handler.lab_score_all(lab_id, limit)
    return result

@server.get('/score/levenshtein')
async def lab_score_levenshtein(lab_id: int, limit: int = None):
    similars = await handler.lab_score_levenshtein(lab_id, limit)
    return similars

if __name__ == '__main__':
    uvicorn.run('server:server', port = 5050, reload = True)
    