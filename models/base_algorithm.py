from api.utils.lab_processing import LabProcessing


class BaseAlgorithm():

    def __init__(self) -> None:
        self.lab_processing = LabProcessing()

    async def check(self, lab_id: int):
        labs = await self.lab_processing.get_labs(lab_id)
        similars = []

        for code, lab in labs:
            distance = self.comparison(code, lab['code'])
            similars.append({'id': lab['id'], 'score': distance})

        return similars

    def comparison(self, str1: str, str2: str) -> float:
        raise NotImplementedError
