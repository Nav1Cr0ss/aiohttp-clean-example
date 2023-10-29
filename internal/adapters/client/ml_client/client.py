from internal.domain.file import DrawingStatusEnum
from pkg.client.aiohttp.client import AioHttpClient


class MLClient(AioHttpClient):
    async def send_drawing_status(
        self, file_id: int, status: DrawingStatusEnum
    ) -> bool:
        endpoint = "/custom_endpoint"
        headers = {"Authorization": "Bearer token"}

        status_code, response_data = await self._post(
            endpoint, headers=headers, data={"file_id": file_id, "status": status}
        )
        # Very confident client :)
        return True
