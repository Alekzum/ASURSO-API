from asurso_api import enums, classes
from . import sync_asurso


def test_login():
    login_success = sync_asurso.login()
    assert isinstance(login_success, bool)


def test_attestation():
    attestation = sync_asurso.get_attestation()
    assert isinstance(attestation, classes.Attestation)


def test_chats():
    chats = sync_asurso.get_chats()
    assert isinstance(chats, list) and (
        chats and isinstance(chats[0], classes.Chat) or True
    )


def test_current_perfomance():
    current_perfomance = sync_asurso.get_current_perfomance()
    assert isinstance(current_perfomance, classes.CurrentPerfomance)


def test_dashboard():
    dashboard = sync_asurso.get_dashboard()
    assert isinstance(dashboard, classes.Dashboard)


def test_group_attestation():
    group_attestation = sync_asurso.get_group_attestation()
    assert isinstance(group_attestation, classes.GroupAttestation)


def test_info():
    info = sync_asurso.get_info()
    assert isinstance(info, classes.Info)


def test_lessons():
    lessons = sync_asurso.get_lessons()
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )


def test_organization():
    organization = sync_asurso.get_organization()
    assert isinstance(organization, classes.Organization)


def test_enum_lessons():
    lessons = sync_asurso.get_lessons(enums.LessonsPeriod.NEXT_DAY)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )
    print(f"Lessons for next day: {lessons}")


def test_logout():
    logout_success = sync_asurso.logout()
    assert isinstance(logout_success, bool)


def test_context():
    with sync_asurso:
        info = sync_asurso.get_info()
    assert isinstance(info, classes.Info)
