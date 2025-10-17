from . import async_asurso, sync_asurso, mark_asyncio, pytest, wrap_coro
from asurso_api import enums, classes
from typing import Union
import datetime


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_login(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    login_info = await wrap_coro(asurso.login(is_remember=False))
    assert isinstance(login_info.tenant_name, str)
    assert isinstance(login_info.tenants[login_info.tenant_name], classes.login.Spo)
    
    assert isinstance(login_info, classes.LoginInfoTemp)
    assert isinstance(login_info.cookies_UID, str)
    assert login_info.cookies_AspNetCoreCookies is None
    assert isinstance(login_info.cookies_AspNetCoreSession, str)

    login_info2 = await wrap_coro(asurso.login(is_remember=True))
    assert isinstance(login_info2, classes.LoginInfoPerm)
    assert isinstance(login_info2.cookies_AspNetCoreCookies, str)
    assert login_info2.cookies_AspNetCoreSession is None


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_attestation(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    attestation = await wrap_coro(asurso.get_attestation())
    print(attestation)
    assert isinstance(attestation, classes.Attestation)

    for year in attestation.academic_years or []:
        assert isinstance(year, classes.attestation.AcademicYear)
        for term in year.terms:
            assert isinstance(term, classes.attestation.Term)
            break
        break


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_chats(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    chats = await wrap_coro(asurso.get_chats())
    print(chats)
    assert isinstance(chats, list)

    for chat in chats:
        assert isinstance(chat, classes.Chat)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_current_performance(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    current_performance = await wrap_coro(asurso.get_current_performance())
    print(current_performance)
    assert isinstance(current_performance, classes.CurrentPerformance)

    for days in current_performance.days_with_marks_for_subject:
        for day in days.days_with_marks:
            assert isinstance(day.day, datetime.date)
            assert isinstance(day.mark, str)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_dashboard(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    dashboard = await wrap_coro(asurso.get_dashboard())
    print(dashboard)
    assert isinstance(dashboard, classes.Dashboard)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_group_attestation(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    group_attestation = await wrap_coro(asurso.get_group_attestation())
    print(group_attestation)
    assert isinstance(group_attestation, classes.GroupAttestation)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_info(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    info = await wrap_coro(asurso.get_info())
    print(info)
    assert isinstance(info, classes.Info)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_lessons(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    lessons = await wrap_coro(asurso.get_lessons())
    print(lessons)
    assert isinstance(lessons, list)
    for lesson in lessons:
        assert isinstance(lesson, classes.LessonsDay)
        assert isinstance(lesson.date, datetime.date)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_organization(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    organization = await wrap_coro(asurso.get_organization())
    print(organization)
    assert isinstance(organization, classes.Organization)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_enum_lessons(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    lessons = await wrap_coro(asurso.get_lessons(enums.LessonsPeriod.NEXT_DAY))
    print(lessons)
    assert isinstance(lessons, list)
    for lesson in lessons:
        assert isinstance(lesson, classes.LessonsDay)
        assert isinstance(lesson.date, datetime.date)
    print(f"Lessons for next day: {lessons}")


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_logout(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    logout_success = await wrap_coro(asurso.logout())
    print(logout_success)
    assert isinstance(logout_success, bool)


@mark_asyncio
@pytest.mark.parametrize("asurso", [async_asurso, sync_asurso])
async def test_context(asurso: Union[classes.ASURSO, classes.AsyncASURSO]):
    async with async_asurso:
        info = await wrap_coro(asurso.get_info())
    print(info)
    assert isinstance(info, classes.Info)
