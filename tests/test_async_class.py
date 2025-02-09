from . import async_asurso
import pytest


pytestmark = pytest.mark.asyncio(loop_scope="module")


@pytestmark
async def test_login():
    await async_asurso.login()


@pytestmark
async def test_attestation():
    await async_asurso.get_attestation()


@pytestmark
async def test_chats():
    await async_asurso.get_chats()


@pytestmark
async def test_current_perfomance():
    await async_asurso.get_current_perfomance()


@pytestmark
async def test_dashboard():
    await async_asurso.get_dashboard()


@pytestmark
async def test_group_attestation():
    await async_asurso.get_group_attestation()


@pytestmark
async def test_info():
    await async_asurso.get_info()


@pytestmark
async def test_lessons():
    await async_asurso.get_lessons()


@pytestmark
async def test_organization():
    await async_asurso.get_organization()


@pytestmark
async def test_logout():
    await async_asurso.logout()


@pytestmark
async def test_context():
    async with async_asurso as asyns_asurso2:
        await asyns_asurso2.get_info()