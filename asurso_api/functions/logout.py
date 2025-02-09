from ..utils import hash_password
from typing import Protocol
import logging
import httpx


logger = logging.getLogger(__name__)


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


async def logout_async(client: httpx.AsyncClient) -> bool:
    r = await client.delete("/services/security/logout")

    client.cookies.update(r.cookies)

    if r.status_code != 200:
        logger.error(f"{r=}, {r.text=}, {r.status_code=}")

    return r.status_code == 200


def logout_sync(client: httpx.Client) -> bool:
    r = client.delete("/services/security/logout")

    client.cookies.update(r.cookies)

    if r.status_code != 200:
        logger.error(f"{r=}, {r.text=}, {r.status_code=}")

    return r.status_code == 200


class AsyncLogoutMethod:
    async def logout(self: AsyncASURSO):
        return await logout_async(self._client)


class LogoutMethod:
    def logout(self: ASURSO):
        return logout_sync(self._client)
