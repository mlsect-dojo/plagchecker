from pathlib import Path
import os
import re

from api.utils.sqliteconnector import SQLiteConnector
from api.utils.lab_processing import LabProcessing


class BaseCheck():

    def __init__(self) -> None:
        self.connector = SQLiteConnector()
        self.lab_processing = LabProcessing()
        self.base_path = Path(__file__).parent.parent.parent.resolve()

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
                    print(lab_folder, lab_file)
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