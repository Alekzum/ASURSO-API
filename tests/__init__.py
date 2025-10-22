from asurso_api import ASURSO, AsyncASURSO
from asurso_api.utils import MyClient, MyAsyncClient
from inspect import iscoroutine
from typing import TypeVar, Coroutine, Any, Union, cast, Literal
import pathlib
import dotenv
import pytest
import json
import os


dotenv.load_dotenv(".env")

env = os.environ
mark = pytest.mark
mark_test_class = pytest.mark.test_classes
mark_asyncio = mark.asyncio(loop_scope="package")
async_client = MyAsyncClient(base_url="https://spo.asurso.ru", timeout=30)
sync_client = MyClient(base_url="https://spo.asurso.ru", timeout=30)

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


@pytest.fixture
async def rejoin_asurso():
    for asurso in (async_asurso, sync_asurso):
        if asurso._logged:
            await wrap_coro(asurso.logout())
        asurso._client.headers.clear()
        asurso._client.cookies.clear()


async def wrap_coro(pre: Union[T, Coroutine[Any, Any, T]]) -> T:
    if iscoroutine(pre):
        result = await pre
    else:
        result = cast(T, pre)
    return result


def get_test_data(
    name: Literal[
        "attestation",
        "chats",
        "dashboard",
        "info",
        "lessons",
        "login",
        "organization",
        "report_current_performance",
        "report_group_attestation",
    ],
):
    return json.loads(pathlib.Path("tests", "test_data", name + ".json").read_text())


__all__ = []  # and __all__ to this __init__ too :P
