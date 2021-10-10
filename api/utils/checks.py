import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import aiofiles

from api.utils.sqliteconnector import SQLiteConnector
from models.Jaccard import jaccard
from models.levenshtein import levenshtein


class LabProcessing():

    def __init__(self) -> None:
        self.connector = SQLiteConnector()
        self.base_path = Path(__file__).parent.parent.resolve()

    async def unpack_archive(self, path: Path) -> TemporaryDirectory:
        archive_dir = TemporaryDirectory(dir = str(Path.joinpath(self.base_path, 'labs')))

        with ZipFile(path) as zip:
            zip.extractall(archive_dir.name)

        return archive_dir

    async def cleanup_archive(self, directory: TemporaryDirectory) -> None:
        directory.cleanup()

    async def get_lab_code(self, path: Path, ext: str) -> str:
        archive_dir = await self.unpack_archive(path)
        folder, files = [file for file in os.walk(archive_dir.name)][-1][::2]
        code = ''
        extension = re.compile(r'.*\.' + f'({ext})' + '{1}$')

        for file in files:
            if extension.match(file):
                async with aiofiles.open(folder + '/' + file, 'r') as f:
                    code += await f.read()

        await self.cleanup_archive(archive_dir)

        return code
        
class BaseCheck():

    def __init__(self) -> None:
        self.connector = SQLiteConnector()
        self.lab_processing = LabProcessing()
        self.base_path = Path(__file__).parent.parent.resolve()

    async def check(self, lab_id: int) -> list:
        lab_info = await self.connector.get_lab_info_id(lab_id)

        if lab_info:
            filename = lab_info['filename']
            lab_path = Path.joinpath(self.base_path,  f'labs/{filename}')
            code = await self.lab_processing.get_lab_code(lab_path, lab_info['ext'])

            lab_folder, lab_files = [file for file in os.walk(Path.joinpath(self.base_path, 'labs'))][-1][::2]
            lab_expr = re.compile(r'.*\.(zip){1}$')

            similars = []

            for lab_file in lab_files:
                if lab_expr.match(lab_file) and lab_file != filename:
                    comparison_lab_info = await self.connector.get_lab_info_filename(lab_file)
                    if comparison_lab_info['ext'] == lab_info['ext'] and comparison_lab_info['user_id'] != lab_info['user_id']:

                        lab = await self.lab_processing.get_lab_code(Path(lab_folder + '/' + lab_file), comparison_lab_info['ext'])
                        distance = await self.algorithm(code, lab)
                        similars.append({'id': comparison_lab_info['lab_id'], 'score': distance})

            return similars

        else:
            return []

    async def algorithm(self, code: str, lab: str) -> float:
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError

class Levenshtein(BaseCheck):

    async def algorithm(self, code: str, lab: str) -> float:
        return levenshtein.distance(code, lab)

    def name(self) -> str:
        return self.__class__.__name__.lower()

class Jaccard(BaseCheck):

    async def algorithm(self, code: str, lab: str) -> float:
        return jaccard.JaccardIndex(code, lab)

    def name(self) -> str:
        return self.__class__.__name__.lower()
