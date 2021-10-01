import pathlib
import uuid

import aiofiles
import aiofiles.os
from fastapi.datastructures import UploadFile

from api.utils.checks import Checks
from api.utils.sqliteconnector import SQLiteConnector


class Handler():

    def __init__(self) -> None:
        self.connector = SQLiteConnector()
        self.checks = Checks()

    async def save_lab(self, user_id: int, ext: str, archive: UploadFile) -> int:
        filename = f'{uuid.uuid4()}.zip'
        data = archive.file.read()
        async with aiofiles.open(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{filename}', 'wb') as file:
            await file.write(data)

        lab_id = await self.connector.insert_lab(f'{filename}', user_id, ext)
        return lab_id

    async def delete_lab(self, lab_id: int):
        path = await self.connector.delete_lab(lab_id)

        if path:
            await aiofiles.os.remove(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{path}')
        return

    async def lab_score_levenshtein(self, lab_id: int, limit: int = None) -> dict:
        levenshtein_result = await self.connector.get_lab_score(lab_id, 'levenshtein_check')
        
        if levenshtein_result != []:
            levenshtein_score = {'similars': [{'id': result['id'], 'score': result['score']} for result in levenshtein_result]}
        else:
            levenshtein_score = await self.checks.levenshtein_check(False, lab_id, limit)
            results = [(item['id'], item['score']) for item in levenshtein_score['similars']]
            await self.connector.save_lab_score(lab_id, self.checks.levenshtein_check.__name__, results)

        return levenshtein_score

    async def lab_score_all(self, lab_id: int, limit: int = None) -> dict:
        levenshtein_result = await self.connector.get_lab_score(lab_id, self.checks.levenshtein_check.__name__)
        jaccard_result = await self.connector.get_lab_score(lab_id, self.checks.jaccard_check.__name__)

        if levenshtein_result != []:
            levenshtein_score = {'similars': [{'id': result['id'], 'score': result['score']} for result in levenshtein_result]}
        else:
            levenshtein_score = await self.checks.levenshtein_check(False, lab_id, limit)
            results = [(item['id'], item['score']) for item in levenshtein_score['similars']]
            await self.connector.save_lab_score(lab_id, self.checks.levenshtein_check.__name__, results)

        if jaccard_result != []:
            jaccard_score = {'similars': [{'id': result['id'], 'score': result['score']} for result in jaccard_result]}
        else:
            jaccard_score = await self.checks.jaccard_check(True, lab_id, limit)
            results = [(item['id'], item['score']) for item in jaccard_score['similars']]
            await self.connector.save_lab_score(lab_id, self.checks.jaccard_check.__name__, results)

        result = {
            'similars': [
                {
                    'algorithm': self.checks.levenshtein_check.__name__,
                    'top': levenshtein_score['similars']
                },
                {
                    'algorithm': self.checks.jaccard_check.__name__,
                    'top': jaccard_score['similars']
                }
            ]
        }
        
        return result
