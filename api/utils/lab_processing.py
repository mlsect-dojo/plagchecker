from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import re
import os
from typing import List, Tuple, Union

import aiofiles

from api.utils.sqliteconnector import SQLiteConnector


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

    async def get_comparison_lab(self, lab_file: str, lab_folder: str, lab_info: dict) -> Union[dict, None]:
        comparison_lab_info = await self.connector.get_lab_info_filename(lab_file)
        if comparison_lab_info['ext'] == lab_info['ext'] and comparison_lab_info['user_id'] != lab_info['user_id']:
            lab_code = await self.get_lab_code(Path(lab_folder + '/' + lab_file), comparison_lab_info['ext'])
            return {'code': lab_code, 'id': comparison_lab_info['lab_id']}

        return None

    async def get_labs(self, lab_id: int) -> List[Tuple[str, dict]]:
        lab_info = await self.connector.get_lab_info_id(lab_id)

        if lab_info:
            results = []

            filename = lab_info['filename']
            lab_path = Path.joinpath(self.base_path,  f'labs/{filename}')
            code = await self.get_lab_code(lab_path, lab_info['ext'])

            lab_folder, lab_files = [file for file in os.walk(Path.joinpath(self.base_path, 'labs'))][-1][::2]
            lab_expr = re.compile(r'.*\.(zip){1}$')

            for lab_file in lab_files:
                if lab_expr.match(lab_file) and lab_file != filename:
                    comparison_lab = await self.get_comparison_lab(lab_file, lab_folder, lab_info)
                    if comparison_lab:
                        results.append((code, comparison_lab))

            return results

        else:
            return []
