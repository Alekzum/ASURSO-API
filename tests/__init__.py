from asurso_api import ASURSO, AsyncASURSO
from asurso_api.utils import MyClient, MyAsyncClient
from inspect import iscoroutine
from typing import TypeVar, Coroutine, Any, Union, cast
import dotenv
import pytest
import os


dotenv.load_dotenv(".env")


pytestmark = pytest.mark.asyncio(loop_scope="package")
pytestmark2 = pytest.mark
async_client = MyAsyncClient(base_url="https://spo.asurso.ru", timeout=30)
sync_client = MyClient(base_url="https://spo.asurso.ru", timeout=30)
env = os.environ

async_asurso = AsyncASURSO(
    login=env["ASURSO_LOGIN"],
    password=env["ASURSO_PASSWORD"],
    timeout=30,
)

sync_asurso = ASURSO(
    login=env["ASURSO_LOGIN"],
    password=env["ASURSO_PASSWORD"],
    timeout=30,
)

T = TypeVar("T")


async def wrap_coro(pre: Union[T, Coroutine[Any, Any, T]]) -> T:
    if iscoroutine(pre):
        result = await pre
    else:
        result = cast(T, pre)
    return result
