from asurso_api import enums, classes
from . import async_asurso
import pytest


pytestmark = pytest.mark.asyncio(loop_scope="module")


@pytestmark
async def test_login():
    login_success = await async_asurso.login()
    assert isinstance(login_success, bool)


@pytestmark
async def test_attestation():
    attestation = await async_asurso.get_attestation()
    assert isinstance(attestation, classes.Attestation)


@pytestmark
async def test_chats():
    chats = await async_asurso.get_chats()
    assert isinstance(chats, list) and (
        chats and isinstance(chats[0], classes.Chat) or True
    )


@pytestmark
async def test_current_perfomance():
    current_perfomance = await async_asurso.get_current_perfomance()
    assert isinstance(current_perfomance, classes.CurrentPerfomance)


@pytestmark
async def test_dashboard():
    dashboard = await async_asurso.get_dashboard()
    assert isinstance(dashboard, classes.Dashboard)


@pytestmark
async def test_group_attestation():
    group_attestation = await async_asurso.get_group_attestation()
    assert isinstance(group_attestation, classes.GroupAttestation)


@pytestmark
async def test_info():
    info = await async_asurso.get_info()
    assert isinstance(info, classes.Info)


@pytestmark
async def test_lessons():
    lessons = await async_asurso.get_lessons()
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )


@pytestmark
async def test_organization():
    organization = await async_asurso.get_organization()
    assert isinstance(organization, classes.Organization)


@pytestmark
async def test_enum_lessons():
    lessons = await async_asurso.get_lessons(enums.LessonsPeriod.NEXT_DAY)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )
    print(f"Lessons for next day: {lessons}")


@pytestmark
async def test_logout():
    logout_success = await async_asurso.logout()
    assert isinstance(logout_success, bool)


@pytestmark
async def test_context():
    async with async_asurso:
        info = await async_asurso.get_info()
    assert isinstance(info, classes.Info)
