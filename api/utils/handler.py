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
        levenshtein_result = await self.connector.get_lab_score(lab_id, 'levenshtein_check')
        
        if levenshtein_result != []:
            result_sorted = sorted(levenshtein_result, key = lambda k: k['score'], reverse = False)
            levenshtein_score = {'similars': [{'id': result['id'], 'score': result['score']} for result in result_sorted]}
        else:
            levenshtein_score = await self.checks.levenshtein_check(False, lab_id)
            results = [(item['id'], item['score']) for item in levenshtein_score['similars']]
            await self.connector.save_lab_score(lab_id, self.checks.levenshtein_check.__name__, results)

        if not limit:
            limit = 10

        return {'similars': levenshtein_score['similars'][:limit]}

    async def lab_score_all(self, lab_id: int, limit: int = None) -> dict:
        result = {'similars': []}
        
        for method, reverse in self.methods:
            method_result = await self.connector.get_lab_score(lab_id, method.__name__)

            if method_result != []:
                result_sorted = sorted(method_result, key = lambda k: k['score'], reverse = reverse)
                method_score = {'similars': [{'id': result['id'], 'score': result['score']} for result in result_sorted]}
            else:
                method_score = await method(reverse,  lab_id)
                results = [(item['id'], item['score']) for item in method_score['similars']]
                await self.connector.save_lab_score(lab_id, method.__name__, results)
            
            if not limit:
                limit = 10

            result['similars'].append({'algorithm': method.__name__, 'top': method_score['similars'][:limit]})
        
        return result
