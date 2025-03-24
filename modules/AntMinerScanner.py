import asyncio
import aiohttp


# **


class AntMinerScanner:
    def __init__(self, subnets: list, excludes: list):
        self.subnets = subnets
        self.excludes = excludes

    async def __is_asic_miner_async(self, ip: str) -> str | None:
        """
        Описание:
        Проверяет, является ли устройство по указанному IP ASIC-майнером

        Параметры:
        ip (str): IP-адрес устройства

        Возвращает:
        str IP-адрес, если устройство ASIC-майнер, иначе None
        """

        url = f"http://{ip}"
        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 401:
                        return ip

        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None

    async def __scan_network_async(self) -> list:
        """
        Описание:
        Сканирует сеть на наличие ASIC-майнеров

        Возвращает:
        List[str]: Список IP-адресов ASIC-майнеров
        """

        asic_miners = []
        async_tasks = []

        for subnet in self.subnets:
            ips = [f"{subnet}.{i}" for i in range(1, 256)]
            async_tasks.extend([self.__is_asic_miner_async(ip) for ip in ips])

        results = await asyncio.gather(*async_tasks)

        # Фильтруем IP-адреса: исключаем те, которые находятся в self.excludes
        filtered_results = filter(lambda ip: ip and ip not in self.excludes, results)
        asic_miners.extend(filtered_results)

        # asic_miners.extend(filter(None, results))

        return asic_miners

    async def get_asic_miners(self) -> None | list:
        """
        Описание:
        Возвращает список IP-адресов ASIC-майнеров в сети

        Возвращает:
        List[str]: список IP-адресов ASIC-майнеров,
        если они найдены, иначе None
        """
        asic_miners = await self.__scan_network_async()
        searched_asics = []

        if asic_miners:
            for miner in asic_miners:
                searched_asics.append(miner)
        else:
            return None

        return searched_asics
