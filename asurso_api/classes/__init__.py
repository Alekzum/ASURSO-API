from ..functions.attestation import Attestation
from ..functions.chats import Chat
from ..functions.dashboard import Dashboard
from ..functions.info import Info
from ..functions.lessons import LessonsDay, Lesson
from ..functions.organization import Organization
from ..functions.reports import GroupAttestation, CurrentPerfomance

from dataclasses import dataclass
from ..functions import AsyncMethods, Methods
from ..functions.utils import hash_password
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
        self.login(True)
        return self

    def __exit__(self, *exc):
        self.logout()
        if exc and any(exc):
            builded_exc = exc[1]
            builded_exc.with_traceback(exc[2])
            raise builded_exc
