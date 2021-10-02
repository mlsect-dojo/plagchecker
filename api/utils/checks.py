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

    def __init__(self) -> None:
        self.connector = SQLiteConnector()
        self.path = pathlib.Path(__file__).parent.parent.resolve()

    async def unpack_archive(self, path: str, ext: str) -> str:
        archive_dir = TemporaryDirectory(dir = str(self.path) + '/labs')
        
        with zipfile.ZipFile(path) as zip:
            zip.extractall(str(archive_dir.name))

        folder, files = [file for file in os.walk(archive_dir.name)][-1][::2]
        code = ''
        extension = re.compile(r'.*\.' + f'({ext})' + '{1}$')

        for file in files:
            if extension.match(file):
                code += open(folder + '/' + file).read()
        archive_dir.cleanup()

        return code

    async def algorithm_check(self, algorithm: Callable[['Checks', int, int], dict], lab_id: int) -> dict:
        lab_info = await self.connector.get_lab_info_id(lab_id)
        if lab_info:
            filename = lab_info['filename']
            code = await self.unpack_archive(f'{self.path}/labs/{filename}', lab_info['ext'])

            lab_folder, lab_files = [file for file in os.walk(f'{str(self.path)}/labs')][-1][::2]
            lab_expr = re.compile(r'.*\.(zip){1}$')

            similars = []

            for lab_file in lab_files:
                if lab_expr.match(lab_file) and lab_file != filename:
                    comparison_lab_info = await self.connector.get_lab_info_filename(lab_file)
                    if comparison_lab_info['ext'] == lab_info['ext'] and comparison_lab_info['user_id'] != lab_info['user_id']:
                        
                        lab = await self.unpack_archive(f'{lab_folder}/{lab_file}', comparison_lab_info['ext'])
                        distance = algorithm(code, lab)
                        similars.append({'id': comparison_lab_info['lab_id'], 'score': distance})

            return similars
        else:
            return []

    async def levenshtein_check(self, lab_id: int) -> dict:
        return await self.algorithm_check(levenshtein.distance, lab_id)

    async def jaccard_check(self, lab_id: int) -> dict:
        return await self.algorithm_check(jaccard.JaccardIndex, lab_id)
