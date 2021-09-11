import os
import pathlib
import re
import zipfile
from tempfile import TemporaryDirectory
from typing import Callable

from api.utils.sqliteconnector import SQLiteConnector
from models.Jaccard import jaccard
from models.levenshtein import levenshtein

class Checks():

    async def algorithm_check(self, algorithm: Callable[['Checks', int, int], dict], list_order: bool, lab_id: int, limit: int = None) -> dict:
        filename = await SQLiteConnector().get_lab_filename(lab_id)
        path = pathlib.Path(__file__).parent.parent.resolve()

        archive_dir = TemporaryDirectory(dir = f'{path}/labs')

        with zipfile.ZipFile(f'{path}/labs/{filename}') as zip:
            zip.extractall(str(archive_dir.name))

        folder, files = [file for file in os.walk(archive_dir.name)][-1][::2]
        code = ''
        extension = re.compile(r'.*\.(c|cs|cpp|dpr|java|scala|py|kt|rb|lisp|go){1}$')
        for file in files:
            if extension.match(file):
                code += open(folder + '/' + file).read()
        archive_dir.cleanup()

        lab_folder, lab_files = [file for file in os.walk(f'{path}/labs')][-1][::2]
        lab_expr = re.compile(r'.*\.(zip){1}$')

        similars = []

        for lab_file in lab_files:
            if lab_expr.match(lab_file) and lab_file != filename:

                lab_file_dir = TemporaryDirectory(dir = f'{path}/labs')

                with zipfile.ZipFile(lab_folder + '/' + lab_file) as zip:
                    zip.extractall(str(lab_file_dir.name))

                folder, files = [file for file in os.walk(lab_file_dir.name)][-1][::2]
                lab = ''
                for file in files:
                    if extension.match(file):
                        lab += open(folder + '/' + file).read()
                lab_file_dir.cleanup()

                distance = algorithm(code, lab)
                lab_id = await SQLiteConnector().get_lab_id(lab_file)
                similars.append({'id': lab_id, 'score': distance})

        similars_final = sorted(similars, key = lambda k: k['score'], reverse = list_order)

        if not limit:
            limit = 10

        return {'similars': similars_final[:limit]}

    async def levenshtein_check(self, list_order: bool, lab_id: int, limit: int = None) -> dict:
        return await self.algorithm_check(levenshtein.distance, list_order, lab_id, limit)

    async def jaccard_check(self, list_order: bool, lab_id: int, limit: int = None) -> dict:
        return await self.algorithm_check(jaccard.JaccardIndex, list_order, lab_id, limit)

    async def check_all(self, lab_id: int, limit: int = None) -> dict:
        top_levenshtein = await self.levenshtein_check(False, lab_id, limit)
        top_jaccard = await self.jaccard_check(True, lab_id, limit)
        return {
            'similars': [
                {
                    'algorithm': 'levenshtein',
                    'top': [
                        top_levenshtein
                    ]
                },
                {
                    'algorithm': 'jaccard',
                    'top': [
                        top_jaccard
                    ]
                }
            ]
        }
        