from asurso_api import functions
from . import sync_client

import os


def test_login():
    r = functions.login.login_sync(
        sync_client,
        os.environ["ASURSO-LOGIN"],
        os.environ["ASURSO-PASSWORD"],
    )
    assert r == True


def test_info():
    info = functions.info.info_sync(sync_client)
    print(info)


def test_dashboard():
    dashboard = functions.dashboard.get_dashboard_sync(
        sync_client, os.environ["ASURSO-SID"]
    )
    print(f"{dashboard=}")


def test_lessons():
    days = functions.lessons.get_lessons_sync(
        sync_client, os.environ["ASURSO-SID"], offset=7
    )
    # print(days[0].model_dump_json(indent=4))

    for day in days:
        print(day.date.split("T")[0])
        for lesson in day.lessons:
            print(
                f"{lesson.name or '*окно*'!r} с {lesson.start_time} до {lesson.end_time}"
            )
        print()
    # print(f"{lessons=}")


def test_organization():
    organization = functions.organization.get_organization_sync(sync_client)


def test_attestation():
    attestation = functions.attestation.get_attestation_sync(
        sync_client, os.environ["ASURSO-SID"]
    )


def test_chats():
    chats = functions.chats.get_chats_sync(sync_client)


def test_reports():
    report1 = functions.reports.get_current_perfomance_sync(
        sync_client, os.environ["ASURSO-SID"]
    )
    report2 = functions.reports.get_group_attestation_sync(
        sync_client, os.environ["ASURSO-SID"]
    )


# if __name__ == "__main__":
#     syncio.run(main())
