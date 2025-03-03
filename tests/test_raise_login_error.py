from . import async_asurso, pytestmark
from asurso_api import exceptions


@pytestmark
async def test_login():
    try:
        chats = await async_asurso.get_chats()
    except Exception as ex:
        assert isinstance(ex, exceptions.UnauthorizedError)
