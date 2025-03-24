import json
from typing import Union
from bos.bosminer.client import BosMiner


# **


class AntMinerData:
    def __init__(self, host: str):
        self.host = host
        self.miner = BosMiner(host)

        self.summary = self.miner.summary()
        self.pools = self.miner.pools()
        self.stats = self.miner.stats()

        # TODO: не удалять, для отладки и просмотра всех параметров!!!
        # formatted_stats = json.dumps(self.stats, indent=4)
        # print(formatted_stats)

    # **

    def get_summary_ghs_current(self) -> float:
        return self.summary["SUMMARY"][0]["GHS 5s"]

    def get_summary_ghs_av(self) -> float:
        return self.summary["SUMMARY"][0]["GHS av"]

    def get_summary_ghs_30_min(self) -> float:
        return self.summary["SUMMARY"][0]["GHS 30m"]

    def get_summary_elapsed(self) -> int:
        return self.summary["SUMMARY"][0]["Elapsed"]

    # **

    def get_pools_user(self) -> str:
        return self.pools["POOLS"][0]["User"]

    # **

    def get_fan_speed(self, fan_number) -> int:
        """
        Описание:
        Получает скорость вращения вентиляторов,
        как правило вентиляторов на AntMiner"s составляет 4шт

        Параметры:
        fan_number (int): Номер вентилятора (1 - 4)

        Возвращает:
        int: скорость вращения вентиляторов
        """
        if 1 <= fan_number <= 4:
            fan = f"fan{fan_number}"
            return self.stats["STATS"][1][fan]

    # **

    def get_temp_chip_on_plate(self, chip_number) -> Union[str, None]:
        """
        Описание:
        Получает температуру чипов на плате по номеру
        2 платы - для E9pro итп
        3 платы - для L7/L9, S21 итп

        key1 - для E9pro/L7/S21
        key2 - для S21pro

        Параметры:
        chip_number (int): Номер платы с чипами (1, 2 или 3)

        Возвращает:
        str: Температура чипов на плату, если существует, иначе None
        """

        key1 = f"temp_in_chip_{chip_number}"
        key2 = f"temp_chip{chip_number}"

        if 1 <= chip_number <= 2:
            if key1 in self.stats["STATS"][1]:
                return self.stats["STATS"][1][key1]
            elif key2 in self.stats["STATS"][1]:
                return self.stats["STATS"][1][key2]
        else:
            temp_chip_plate = None

            try:
                if key1 in self.stats["STATS"][1]:
                    temp_chip_plate = self.stats["STATS"][1][key1]
                elif key2 in self.stats["STATS"][1]:
                    temp_chip_plate = self.stats["STATS"][1][key2]
            except:
                temp_chip_plate = None

            return temp_chip_plate

    # **

    def get_temp_max(self) -> int:
        return self.stats["STATS"][1]["temp_max"]
