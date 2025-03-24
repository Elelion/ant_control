import re
from typing import Union


# **


class AntMinerHelper:
    """
    Описание:
    Класс содержит методы, которые служат как помощники, те они помогают
    конвертировать или извлекать какие либо данные полученные с помощью
    класса AntMinerData
    """

    def __init__(self, worker_name: str, ghs: float):
        self.worker_name = worker_name
        self.ghs = ghs

    @classmethod
    def extract_type_asic_from_name(cls, worker_name: str) -> Union[str, None]:
        """
        Описание:
        Извлекает тип ASIC  из имени воркера

        Параметры:
        worker_name (str): Имя воркера, формата: worker.1-5-3_3780_E9pro

        Возвращает:
        Union[str, None]: E9pro, если найден, иначе None
        """
        if '_' in worker_name:
            return worker_name.split('_')[-1]

        return None

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

        pattern1 = r"\d+_(\d+)_"
        match1 = re.search(pattern1, worker_name)

        if match1:
            result_match = match1.group(1)
            return result_match

        parts = worker_name.split("x")

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

    @classmethod
    def extract_dhm_from_ms(self, ms: int) -> list:
        """
        Описание:
        Преобразует мс в день, час, мин, сек

        Параметры:
        ms (int) - кол-во отработанных мс

        Возвращает:
        list[days, hours, minutes]
        """
        days = ms // 86400
        ms %= 86400

        hours = ms // 3600
        ms %= 3600

        minutes = ms // 60
        ms %= 60

        return [days, hours, minutes]
