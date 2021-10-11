from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import re
import os

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