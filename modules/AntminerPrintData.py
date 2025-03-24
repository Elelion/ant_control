from modules.AntMinerData import AntMinerData


# **


class AntMinerPrintData:
    def __init__(self, miner_data: AntMinerData, miner_helper_cls: type):
        self.miner_data = miner_data
        self.helper = miner_helper_cls

    def print_data(self) -> None:
        """
        Описание:
        Выводит в консоль данные данные об AntMiner

        Параметры:
        Нет

        Возвращает:
        None
        """

        # скорость вентиляторов
        for fan_num in range(1, 5):
            fan_speed = self.miner_data.get_fan_speed(fan_num)
            print(f"fan{fan_num}: {fan_speed}", end=", " if fan_num < 4 else "\n")

        # температура чипов
        for plate_num in range(1, 4):
            print(f"plate {plate_num}:", self.miner_data.get_temp_chip_on_plate(plate_num))

        print("ghs av:", self.miner_data.get_summary_ghs_av())
        print("ghs 30 min:", self.miner_data.get_summary_ghs_30_min())
        print("ghs current:", self.miner_data.get_summary_ghs_current())

        days, hours, minutes = self.helper.extract_dhm_from_ms(self.miner_data.get_summary_elapsed())
        print("elapsed: {} ms, or {} days, {} hours, {} minutes".format(
                self.miner_data.get_summary_elapsed(),
                days, hours, minutes
            )
        )

        print("pool name:", self.miner_data.get_pools_user())

        print("max temp:", self.miner_data.get_temp_max())

        print("hash from name: {}".format(
            self.helper.extract_hash_rate_from_name(
                self.miner_data.get_pools_user()
            )
        ))

        print("-" * 20)
