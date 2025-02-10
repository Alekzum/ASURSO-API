from dataclasses import dataclass
from ..functions import AsyncMethods, Methods
from ..utils import hash_password
import contextlib
import httpx


@dataclass
class AsyncASURSO(AsyncMethods):
    _login: str
    _password: str
    _SID: str
    _client: httpx.AsyncClient

    def __init__(self, login: str, password: str, SID: str):
        """Just create ASURSO object to use this API

        Args:
            login (str): your login
            password (str): your password
            SID (str): get via DevTools please
        """
        self._login = login
        self._password = hash_password(password)

        self._SID = SID
        self._client = httpx.AsyncClient(base_url="https://spo.asurso.ru")

    async def __aenter__(self):
        await self.login()
        return self

    async def __aexit__(self, *exc):
        await self.logout()
        if exc and any(exc):
            raise Exception(*exc)


@dataclass
class ASURSO(Methods):
    _login: str
    _password: str
    _SID: str
    _client: httpx.Client

    def __init__(self, login: str, password: str, SID: str):
        """Just create ASURSO object to use this API

        Args:
            login (str): your login
            password (str): your password
            SID (str): get via DevTools please
        """
        self._login = login
        self._password = hash_password(password)

        self._SID = SID
        self._client = httpx.Client(base_url="https://spo.asurso.ru")

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *exc):
        self.logout()
        if exc and any(exc):
            raise Exception(*exc)
