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


async def login_async(
    client: httpx.AsyncClient,
    login: str,
    password: str,
    is_remember=False,
    need_to_hash=True,
) -> bool:
    if need_to_hash:
        password = hash_password(password)

    r = await client.post(
        "/services/security/login",
        json=dict(login=login, password=password, isRemember=is_remember),
    )

    client.cookies.update(r.cookies)

    if r.status_code != 200:
        logger.error(f"{r=}, {r.text=}, {r.status_code=}")

    return r.status_code == 200


def login_sync(
    client: httpx.Client,
    login: str,
    password: str,
    is_remember=False,
    need_to_hash=True,
) -> bool:
    if need_to_hash:
        password = hash_password(password)

    r = client.post(
        "/services/security/login",
        json=dict(login=login, password=password, isRemember=is_remember),
    )

    client.cookies.update(r.cookies)

    if r.status_code != 200:
        logger.error(f"{r=}, {r.text=}, {r.status_code=}")

    return r.status_code == 200


class AsyncLoginMethod:
    async def login(self: AsyncASURSO, isRemember=False):
        return await login_async(
            self._client, self._login, self._password, isRemember, need_to_hash=False
        )


class LoginMethod:
    def login(self: ASURSO, isRemember=False):
        return login_sync(
            self._client, self._login, self._password, isRemember, need_to_hash=False
        )
