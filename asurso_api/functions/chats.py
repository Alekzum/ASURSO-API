from pydantic import BaseModel, Field
from typing import Protocol, List
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


class Chat(BaseModel):
    num: int
    id: int
    name: str
    chat_type: str = Field(..., alias="chatType")
    count_of_members: int = Field(..., alias="countOfMembers")
    admin_name: str = Field(..., alias="adminName")


async def get_chats_async(client: httpx.AsyncClient) -> List[Chat]:
    r = await client.get("/integration/chatManagement/chats/current")
    data = r.json()
    return [Chat(**i) for i in data]


def get_chats_sync(client: httpx.Client) -> List[Chat]:
    r = client.get("/integration/chatManagement/chats/current")
    data = r.json()
    return [Chat(**i) for i in data]


class AsyncGetChatsMethod:
    async def get_chats(self: AsyncASURSO) -> List[Chat]:
        return await get_chats_async(self._client)


class GetChatsMethod:
    def get_chats(self: ASURSO) -> List[Chat]:
        return get_chats_sync(self._client)
