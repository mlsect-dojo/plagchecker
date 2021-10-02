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
        self.methods = [
            (self.checks.levenshtein_check, False),
            (self.checks.jaccard_check, True)
        ]

    async def save_lab(self, user_id: int, ext: str, archive: UploadFile) -> int:
        filename = f'{uuid.uuid4()}.zip'
        data = archive.file.read()
        
        async with aiofiles.open(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{filename}', 'wb') as file:
            await file.write(data)

        lab_id = await self.connector.insert_lab(f'{filename}', user_id, ext)
        return lab_id

    async def delete_lab(self, lab_id: int) -> None:
        path = await self.connector.delete_lab(lab_id)

        if path:
            await aiofiles.os.remove(f'{pathlib.Path(__file__).parent.resolve()}/api/labs/{path}')

        return

    async def lab_score_levenshtein(self, lab_id: int, limit: int = None) -> dict:
        db_result = await self.connector.get_lab_score(lab_id, 'levenshtein_check')
        
        if db_result != []:
            result_sorted = sorted(db_result, key = lambda k: k['score'], reverse = False)
            levenshtein_score = [{'id': result['id'], 'score': result['score']} for result in result_sorted]
        else:
            check_result = await self.checks.levenshtein_check(False, lab_id)
            levenshtein_score = sorted(check_result, key = lambda k: k['score'], reverse = False)
            results = [(item['id'], item['score']) for item in levenshtein_score]
            await self.connector.save_lab_score(lab_id, self.checks.levenshtein_check.__name__, results)

        if not limit:
            limit = 10

        return {'similars': levenshtein_score[:limit]}

    async def lab_score_all(self, lab_id: int, limit: int = None) -> dict:
        result = {'similars': []}
        
        for algorithm, reverse in self.methods:
            db_result = await self.connector.get_lab_score(lab_id, algorithm.__name__)

            if db_result != []:
                result_sorted = sorted(db_result, key = lambda k: k['score'], reverse = reverse)
                algorithm_result = [{'id': result['id'], 'score': result['score']} for result in result_sorted]
            else:
                check_result = await algorithm(lab_id)
                algorithm_result = sorted(check_result, key = lambda k: k['score'], reverse = reverse)
                results = [(item['id'], item['score']) for item in algorithm_result]
                await self.connector.save_lab_score(lab_id, algorithm.__name__, results)
            
            if not limit:
                limit = 10

            result['similars'].append({
                'algorithm': algorithm.__name__,
                'top': algorithm_result[:limit]
            })
        
        return result
