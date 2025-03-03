from . import async_client, pytestmark
from asurso_api import functions, enums, classes
import os


LOGIN = os.environ["ASURSO_LOGIN"]
SID = os.environ["ASURSO_SID"]


@pytestmark
async def test_login():
    login_success = await functions.login.login_async(
        async_client,
        os.environ["ASURSO_LOGIN"],
        os.environ["ASURSO_PASSWORD"],
    )
    assert isinstance(login_success, classes.LoginInfo)


@pytestmark
async def test_attestation():
    attestation = await functions.attestation.get_attestation_async(
        client=async_client, SID=SID
    )
    assert isinstance(attestation, classes.Attestation)


@pytestmark
async def test_chats():
    chats = await functions.chats.get_chats_async(client=async_client)
    assert isinstance(chats, list) and (
        chats and isinstance(chats[0], classes.Chat) or True
    )


@pytestmark
async def test_current_performance():
    current_performance = await functions.reports.get_current_performance_async(
        client=async_client, SID=SID
    )
    assert isinstance(current_performance, classes.CurrentPerformance)


@pytestmark
async def test_dashboard():
    dashboard = await functions.dashboard.get_dashboard_async(
        client=async_client, SID=SID
    )
    assert isinstance(dashboard, classes.Dashboard)


@pytestmark
async def test_group_attestation():
    group_attestation = await functions.reports.get_group_attestation_async(
        client=async_client, SID=SID
    )
    assert isinstance(group_attestation, classes.GroupAttestation)


@pytestmark
async def test_info():
    info = await functions.info.get_info_async(client=async_client)
    assert isinstance(info, classes.Info)


@pytestmark
async def test_lessons():
    lessons = await functions.lessons.get_lessons_async(client=async_client, SID=SID)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )


@pytestmark
async def test_organization():
    organization = await functions.organization.get_organization_async(
        client=async_client
    )
    assert isinstance(organization, classes.Organization)


@pytestmark
async def test_enum_lessons():
    lessons = await functions.lessons.get_lessons_async(
        client=async_client, SID=SID, start=enums.LessonsPeriod.NEXT_DAY
    )
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )
    print(f"Lessons for next day: {lessons}")


@pytestmark
async def test_logout():
    logout_success = await functions.logout.logout_async(client=async_client)
    assert isinstance(logout_success, bool)
