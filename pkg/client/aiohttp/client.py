import aiohttp


class AioHttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def __request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, params=params, data=data, headers=headers
            ) as response:
                response_data = await response.text()
                return response.status, response_data

    async def _get(self, endpoint, params=None, headers=None):
        return await self.__request("GET", endpoint, params=params, headers=headers)

    async def _post(self, endpoint, data=None, headers=None):
        return await self.__request("POST", endpoint, data=data, headers=headers)

    async def _put(self, endpoint, data=None, headers=None):
        return await self.__request("PUT", endpoint, data=data, headers=headers)

    async def _delete(self, endpoint, headers=None):
        return await self.__request("DELETE", endpoint, headers=headers)
