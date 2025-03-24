import asyncio
from typing import Final

from modules.AntMinerControl import AntMinerControl
from modules.AntMinerData import AntMinerData
from modules.AntMinerHelper import AntMinerHelper
from modules.AntMinerScanner import AntMinerScanner
from modules.AntminerPrintData import AntMinerPrintData
from modules.MailSend import MailSend

# -----------------------------------------------------------------------------


SUBNETS: Final[list[str]] = [
    "192.168.0",
    "192.168.1",
    "192.168.2",
    "192.168.3",
    "192.168.4",
    "192.168.5",
    "192.168.6",
    "192.168.7",
    "192.168.8",
    "192.168.9",
]

IP_EXCLUDES: Final[list[str]] = [
    '192.168.6.157',
    # '192.168.0.101'
]

scan = AntMinerScanner(SUBNETS, IP_EXCLUDES)
scan_miner_list = asyncio.run(scan.get_asic_miners())

# **

if scan_miner_list:
    print("Найденные AntMiner:", len(scan_miner_list))

    for miner_ip in scan_miner_list:
        print("-> ip:", miner_ip)

        # вывод данных об майнере в консоль
        miner_data = AntMinerData(miner_ip)
        # print_data_asics = AntMinerPrintData(miner_data, AntMinerHelper)
        # print_data_asics.print_data()

        # **

        # .control - метод, анализирующий ошибки, и отправляющий уведомления
        miner_control = AntMinerControl(
            miner_ip,
            miner_data,
            AntMinerHelper,
            MailSend
        )
        miner_control.control()
else:
    print("ASIC майнеры не найдены.")
