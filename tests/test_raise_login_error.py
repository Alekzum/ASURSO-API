from . import async_asurso, sync_asurso, pytestmark, pytest, wrap_coro
from asurso_api import exceptions, classes
from typing import Union
import datetime

@pytestmark
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_login(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    try:
        await wrap_coro(asurso.get_chats())
    except Exception as ex:
        assert isinstance(ex, exceptions.UnauthorizedError)
