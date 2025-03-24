from typing import Final, List

from modules.AntMinerData import AntMinerData
from modules.MailSend import MailSend


# **


class AntMinerControl:
    # TODO:
    #  temperatures - готово
    #  uptime - готово, в hashrate
    #  hashrate -
    #  fans - готово

    def __init__(
            self,
            miner_ip: str,
            miner_data: AntMinerData,
            miner_helper_cls: type,
            mail: type
    ):
        # temperatures
        self.TEMP_PLATE_MAX: Final = 85.0
        self.TEMP_PLATE_MIN: Final = 20.0
        self.HASH_RATE_DIFFERENCE: Final = 5

        # hash-rates
        self.MHS_VALUES = {
            "S21XP": 265.0,
            "S21PRO": 225.0,
            "S21": 185.0,
            "S19": 115.0,
            "E9PRO": 3500.0,
            "L7": 8700.0,
            "L9": 15.0
        }

        # fans
        self.FAN_SPEED_MIN = 1500
        self.FAN_SPEED_MAX = 6500

        # uptime
        self.UPTIME_MINUTES_MIN = 50

        # **

        # for email
        self.msg_data = {}
        self.msg_status = False

        # **

        self.miner_ip = miner_ip
        self.miner_data = miner_data
        self.miner_helper = miner_helper_cls
        self.mail = mail

        # **

        self.DAYS, self.HOURS, self.MINUTES = self.miner_helper.extract_dhm_from_ms(
            self.miner_data.get_summary_elapsed()
        )

    def control(self) -> None:
        """
        Описание:
        Вызывает private методы класса, где каждый метод выполняет
        возложенную на него роль

        Параметры:
        Нет

        Возвращает:
        None
        """

        self.__control_temperatures()
        self.__control_fans()
        self.__control_hash_rate()
        self.__send_mail()

    # **

    def __control_temperatures(self) -> None:
        """
        Описание:
        Метод для мониторинга температуры на платах майнера

        - Получает температуры с двух/трёх плат майнера с помощью вызова
        метода `get_temp_chip_on_plate`

        - Формирует сообщение о текущих температурах и максимальной
        зафиксированной температуре

        - Проверяет корректность температур с помощью
        метода `__temperatures_check`. Если есть превышение допустимых значений,
        формирует и выводит сообщение с предупреждением

        Параметры:
        Нет

        Возвращает:
        None
        """

        temp_list = []
        for plate_num in range(1, 4):
            temp_list.append(self.miner_data.get_temp_chip_on_plate(plate_num))

        if self.__is_temperatures_check(temp_list):
            temp_data = {
                "Plates temp": temp_list,
                "Max temp": self.miner_data.get_temp_max(),
            }

            self.msg_data["temp_data"], self.msg_status = temp_data, True

    def __is_temperatures_check(self, temp_list: List[str]) -> bool:
        """
        Описание:
        Проверяет список строк с температурами. Пробегаемся по:
        plate 1: 51-54-65-68
        plate 2: 53-54-65-80
        plate 3: None
        и собираем в list температуры, в формате: [48.0, 51.0, ...]

        Параметры:
        temp_list - список со строками температур

        Возвращает:
        False - Все температуры в пределах допустимого диапазона
        True - Если хотя бы одно значение выходит за пределы
        """

        temperatures = []
        for t in temp_list:
            # Пропускаем значения если None
            if t is None:
                continue

            try:
                # Преобразуем строку в list, типа: [48.0, 51.0, 64.0, 65.0]
                # Склеивая каждую строку с температурами в один list[...]
                temperatures.extend([float(temp) for temp in t.split("-")])
            except ValueError:
                # Возвращаем False, если не удается преобразовать строку в числа
                return True

        # Проверяем каждую температуру
        for t in temperatures:
            if t > self.TEMP_PLATE_MAX or t < self.TEMP_PLATE_MIN:
                print(f"- Temperature {t} out of range!")
                return True

        return False

    # **

    def __control_fans(self) -> None:
        """
        Описание:
        Метод для мониторинга скорости вентиляторов

        - Получает обороты с четырех вентиляторов майнера с помощью вызова
        метода `get_temp_chip_on_plate`

        - Формирует сообщение о текущих оборотах

        - Проверяет корректность оборотов с помощью
        метода `__fans_check`. Если есть превышение допустимых значений,
        формирует и выводит сообщение с предупреждением`

        Параметры:
        Нет

        Возвращает:
        None
        """
        # ip, fan_speed_in, fan_speed_out
        fan_list = []
        for fan_num in range(1, 5):
            fan_list.append(self.miner_data.get_fan_speed(fan_num))

        if self.__is_fans_check(fan_list):
            fans_data = {
                "fans_speed": fan_list,
            }

            self.msg_data["fan_data"], self.msg_status = fans_data, True

    def __is_fans_check(self, fans_list: List[str]) -> bool:
        """
        Описание:
        Проверяет список строк с оборотами. Возвращает False, если хотя
        бы одно значение вне диапазона.

        Параметры:
        fans_list - список со строками оборотов

        Возвращает:
        False - Все обороты в пределах допустимого диапазона
        True - Если хотя бы одно значение выходит за пределы
        """

        # Проверяем каждый вентилятор
        for fan in fans_list:
            if int(fan) > self.FAN_SPEED_MAX or int(fan) < self.FAN_SPEED_MIN:
                return True

        return False

    # **

    def __control_hash_rate(self):
        """
        Описание:
        chatGPT generation...

        Параметры:
        Нет

        Возвращает:
        None
        """

        ghs_values = [
            self.miner_data.get_summary_ghs_av(),
            self.miner_data.get_summary_ghs_30_min()
        ]

        type_worker = self.miner_helper.extract_type_asic_from_name(
            self.miner_data.get_pools_user()
        )

        # используем match тк могут быть доп обработки для каждого типа
        match type_worker.upper():
            case "S21PRO":
                if self.MINUTES >= 30:
                    self.__hash_rate_check(ghs_values, "S21PRO")

            case "S21":
                if self.MINUTES >= 30:
                    self.__hash_rate_check(ghs_values, "S21")

            case "S19":
                if self.MINUTES >= 50:
                    self.__hash_rate_check(ghs_values, "S19")

            case "E9PRO":
                if self.HOURS >= 1:
                    self.__hash_rate_check(ghs_values, "E9PRO")

            case "L7":
                if self.MINUTES >= 20:
                    self.__hash_rate_check(ghs_values, "L7")

            case "L9":
                if self.MINUTES >= 20:
                    self.__hash_rate_check(ghs_values, "L9")

            case _:
                # Действия по умолчанию, если ни одно из условий не выполнено
                print("default")

    def __hash_rate_check(self, ghs_values: list, type_worker: str) -> None:
        """
        Описание:
        проверяет av и 30min hash rate аппарата

        Параметры:
        ghs_values - [get_summary_ghs_av, get_summary_ghs_30_min]
        days, hours, minutes - сколько аппарат отработал времени

        Возвращает:
        None
        """

        if self.__is_hash_rate_check(ghs_values, type_worker):
            ghs_data = {
                "ghs av": ghs_values[0],
                "ghs 30 min": ghs_values[1],
                "ghs current": self.miner_data.get_summary_ghs_current(),
                "uptime": f"{self.DAYS} days, {self.HOURS} hours and {self.MINUTES} min",
            }

            self.msg_data["ghs_data"], self.msg_status = ghs_data, True
        else:
            print(f"{type_worker} is ok")

    # **

    def __is_hash_rate_check(self, ghs_list: List[str], asic_type: str) -> bool:
        """
        Описание:
        сверяет значение в List c соответствующим значением в MHS_VALUES: Dict

        Параметры:
        ghs_list - список со строками хеш-рейта
        asic_type - тип асика

        Возвращает:
        False - Если все значения в пределах допустимого диапазона
        True - Если хотя бы одно значение выходит за пределы
        """

        if any(value <= self.MHS_VALUES.get(asic_type) for value in ghs_list):
            print("- Hash-rate out of range!\nav: {}, 30m: {}, current: {}".format(
                ghs_list[0],
                ghs_list[1],
                self.miner_data.get_summary_ghs_current()
            ))

            return True

        return False

    # **

    def __send_mail(self) -> None:
        """
        Описание:
        Для отправки электронной почты с сообщением об неполадке
        Создает объект MailSend и добавляет сообщение о проверке
        ASIC в тело письма

        Параметры:
        Нет

        Возвращает:
        None
        """

        title = f"{self.miner_ip} - Alert!"

        if self.msg_status:
            content_html = self.__html_content(title, self.msg_data)
            self.msg_status = False

            self.mail(title + "\n\n" + content_html)

    def __html_content(self, title: str, content: dict) -> str:
        # FA840B - titles (orange)
        # #ffc300 - text (biruze)

        html_template = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                        }}
                        .container {{
                            margin: 20px;
                            padding: 10px;
                            border: 1px solid #5B5B5B;
                            border-radius: 5px;
                            background-color: #282828;
                        }}
                        .section-title {{
                            font-size: 18px;
                            font-weight: bold;
                            margin-top: 20px;
                            color: #FA840B;
                        }}
                        .section-content {{
                            margin-left: 20px;
                            margin-top: 10px;
                            color: ghostwhite;
                        }}
                        .list-item {{
                            margin-bottom: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2 style='color: #FA840B;'>{title}</h2>
                        <div class="section">
            """

        for key, value in content.items():
            html_template += f'<div class="section-title">{key}:</div>'
            html_template += '<div class="section-content">'

            for sub_key, sub_value in value.items():
                html_template += f'<div class="section-title">{sub_key}:</div>'

                if isinstance(sub_value, list):
                    for item in sub_value:
                        html_template += f'<div class="list-item">{item}</div>'
                else:
                    html_template += f'<div class="list-item">{sub_value}</div>'
            html_template += '</div>'
        html_template += """
                    </div>
                </div>
            </body>
        </html>
        """

        return html_template
