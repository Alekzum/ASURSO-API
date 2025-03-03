from ..utils import parse_response
from typing import List, Protocol
from pydantic import BaseModel
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


class Subject(BaseModel):
    mark: float
    name: str
    id: int


class Dashboard(BaseModel):
    subjects: List[Subject]


async def get_dashboard_async(client: httpx.AsyncClient, SID: str) -> Dashboard:
    r = await client.get(f"services/students/{SID}/dashboard")
    return parse_response(r, Dashboard)


def get_dashboard_sync(client: httpx.Client, SID: str) -> Dashboard:
    r = client.get(f"services/students/{SID}/dashboard")
    return parse_response(r, Dashboard)


class AsyncGetDashboardMethod:
    async def get_dashboard(self: AsyncASURSO) -> Dashboard:
        return await get_dashboard_async(self._client, self._SID)


class GetDashboardMethod:
    def get_dashboard(self: ASURSO) -> Dashboard:
        return get_dashboard_sync(self._client, self._SID)
