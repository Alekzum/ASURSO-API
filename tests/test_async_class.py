from . import async_asurso, pytestmark
from asurso_api import enums, classes


@pytestmark
async def test_login():
    login_success = await async_asurso.login()
    print(login_success)
    assert isinstance(login_success, classes.LoginInfo)


@pytestmark
async def test_attestation():
    attestation = await async_asurso.get_attestation()
    print(attestation)
    assert isinstance(attestation, classes.Attestation)


@pytestmark
async def test_chats():
    chats = await async_asurso.get_chats()
    print(chats)
    assert isinstance(chats, list) and (
        chats and isinstance(chats[0], classes.Chat) or True
    )


@pytestmark
async def test_current_performance():
    current_performance = await async_asurso.get_current_performance()
    print(current_performance)
    assert isinstance(current_performance, classes.CurrentPerformance)


@pytestmark
async def test_dashboard():
    dashboard = await async_asurso.get_dashboard()
    print(dashboard)
    assert isinstance(dashboard, classes.Dashboard)


@pytestmark
async def test_group_attestation():
    group_attestation = await async_asurso.get_group_attestation()
    print(group_attestation)
    assert isinstance(group_attestation, classes.GroupAttestation)


@pytestmark
async def test_info():
    info = await async_asurso.get_info()
    print(info)
    assert isinstance(info, classes.Info)


@pytestmark
async def test_lessons():
    lessons = await async_asurso.get_lessons()
    print(lessons)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )


@pytestmark
async def test_organization():
    organization = await async_asurso.get_organization()
    print(organization)
    assert isinstance(organization, classes.Organization)


@pytestmark
async def test_enum_lessons():
    lessons = await async_asurso.get_lessons(enums.LessonsPeriod.NEXT_DAY)
    print(lessons)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )
    print(f"Lessons for next day: {lessons}")


@pytestmark
async def test_logout():
    logout_success = await async_asurso.logout()
    print(logout_success)
    assert isinstance(logout_success, bool)


@pytestmark
async def test_context():
    async with async_asurso:
        info = await async_asurso.get_info()
    print(info)
    assert isinstance(info, classes.Info)
