import asyncio

from modules import *
from modules.AntMenerData import AntMinerData
from modules.AntMinerHelper import AntMinerHelper
from modules.AntMinerScanner import AntMinerScanner

# -----------------------------------------------------------------------------


SUBNETS = [
    "192.168.0",
    "192.168.1",
    "192.168.2",
    "192.168.3",
    "192.168.4",
    "192.168.5",
    "192.168.6",
    "192.168.7",
    "192.168.8",
    "192.168.9"
]

scan = AntMinerScanner(SUBNETS)
scan_asics = asyncio.run(scan.get_asic_miners())

if scan_asics:
    print("Найденные AntMiner:", len(scan_asics))

    for miner in scan_asics:
        print(miner)
else:
    print("ASIC майнеры не найдены.")

# host = '192.168.0.104'
# antminer = AntMinerData(host)
#
# print("fan1: {}, fan2: {}, fan3: {}, fan4: {}".format(
#     antminer.get_fan_speed(1),
#     antminer.get_fan_speed(2),
#     antminer.get_fan_speed(3),
#     antminer.get_fan_speed(4),
# ))
#
# print("plate 1: ", antminer.get_temp_chip_on_plate(1))
# print("plate 2: ", antminer.get_temp_chip_on_plate(2))
# print("plate 3: ", antminer.get_temp_chip_on_plate(3))
#
# print("ghs av: ", antminer.get_summary_ghs_av())
# print("ghs 30 min: ", antminer.get_summary_ghs_30_min())
# print("ghs current: ", antminer.get_summary_ghs_current())
# print("pool name: ", antminer.get_pools_user())
# print("max temp", antminer.get_temp_max())
#
# print("hash from name:, {}".format(
#     AntMinerHelper.extract_hash_rate_from_name(antminer.get_pools_user())
# ))
