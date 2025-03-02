from asurso_api import functions, enums, classes
from . import sync_client

import os


LOGIN = os.environ["ASURSO_LOGIN"]
SID = os.environ["ASURSO_SID"]


def test_login():
    login_success = functions.login.login_sync(
        sync_client,
        os.environ["ASURSO_LOGIN"],
        os.environ["ASURSO_PASSWORD"],
    )
    assert isinstance(login_success, classes.LoginInfo)


def test_attestation():
    attestation = functions.attestation.get_attestation_sync(
        client=sync_client, SID=SID
    )
    assert isinstance(attestation, classes.Attestation)


def test_chats():
    chats = functions.chats.get_chats_sync(client=sync_client)
    assert isinstance(chats, list) and (
        chats and isinstance(chats[0], classes.Chat) or True
    )


def test_current_performance():
    current_performance = functions.reports.get_current_performance_sync(
        client=sync_client, SID=SID
    )
    assert isinstance(current_performance, classes.CurrentPerformance)


def test_dashboard():
    dashboard = functions.dashboard.get_dashboard_sync(client=sync_client, SID=SID)
    assert isinstance(dashboard, classes.Dashboard)


def test_group_attestation():
    group_attestation = functions.reports.get_group_attestation_sync(
        client=sync_client, SID=SID
    )
    assert isinstance(group_attestation, classes.GroupAttestation)


def test_info():
    info = functions.info.get_info_sync(client=sync_client)
    assert isinstance(info, classes.Info)


def test_lessons():
    lessons = functions.lessons.get_lessons_sync(client=sync_client, SID=SID)
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )


def test_organization():
    organization = functions.organization.get_organization_sync(client=sync_client)
    assert isinstance(organization, classes.Organization)


def test_enum_lessons():
    lessons = functions.lessons.get_lessons_sync(
        client=sync_client, SID=SID, start=enums.LessonsPeriod.NEXT_DAY
    )
    assert isinstance(lessons, list) and (
        lessons and isinstance(lessons[0], classes.LessonsDay) or True
    )
    print(f"Lessons for next day: {lessons}")


def test_logout():
    logout_success = functions.logout.logout_sync(client=sync_client)
    assert isinstance(logout_success, bool)
