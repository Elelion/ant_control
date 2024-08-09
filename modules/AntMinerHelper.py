import re
from typing import Union


# **


class AntMinerHelper:
    def __init__(self, worker_name: str, ghs: float):
        self.worker_name = worker_name
        self.ghs = ghs

    @classmethod
    def extract_hash_rate_from_name(cls, worker_name: str) -> Union[str, None]:
        """
        Описание:
        Извлекает хешрейт из имени воркера

        Параметры:
        worker_name (str): Имя воркера, формата: worker.1-5-3_3780_E9pro

        Возвращает:
        Union[str, None]: Хешрейт, если найден, иначе None
        """

        pattern1 = r'\d+_(\d+)_'
        match1 = re.search(pattern1, worker_name)

        if match1:
            result_match = match1.group(1)
            return result_match

        parts = worker_name.split('x')

        if len(parts) > 3:
            hashrate = parts[3]
            return hashrate

        return None

    @classmethod
    def convert_ghs_to_ths(cls, ghs: float) -> str:
        """
        Описание:
        Преобразует хешрейт из GHS в THS

        Параметры:
        ghs (float): Хешрейт в GHS

        Возвращает:
        str: Хешрейт в THS с точностью до двух знаков после запятой
        """

        hashrate_th = ghs / 1000
        return f"{hashrate_th:.2f}"
