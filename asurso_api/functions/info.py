from typing import Protocol
import httpx


class AsyncASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: httpx.AsyncClient


class ASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: httpx.Client


async def info_async(client: httpx.AsyncClient):
    r = await client.get("/services/people/system/info")
    data = r.json()
    return data


def info_sync(client: httpx.Client):
    r = client.get("/services/people/system/info")
    data = r.json()
    return data


class AsyncGetInfoMethod:
    async def get_info(self: AsyncASURSO):
        return await info_async(self._client)


class GetInfoMethod:
    def get_info(self: ASURSO):
        return info_sync(self._client)