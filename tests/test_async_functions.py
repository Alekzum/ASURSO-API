from asurso_api import functions
from . import async_client

import pytest
import os


pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytestmark
async def test_login():
    r = await functions.login.login_async(
        async_client,
        os.environ["ASURSO_LOGIN"],
        os.environ["ASURSO_PASSWORD"],
    )
    assert r == True


@pytestmark
async def test_info():
    info = await functions.info.info_async(async_client)
    print(info)


@pytestmark
async def test_dashboard():
    dashboard = await functions.dashboard.get_dashboard_async(
        async_client, os.environ["ASURSO_SID"]
    )
    print(f"{dashboard=}")


@pytestmark
async def test_lessons():
    days = await functions.lessons.get_lessons_async(
        async_client, os.environ["ASURSO_SID"], offset=7
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


@pytestmark
async def test_organization():
    organization = await functions.organization.get_organization_async(async_client)


@pytestmark
async def test_attestation():
    attestation = await functions.attestation.get_attestation_async(
        async_client, os.environ["ASURSO_SID"]
    )


@pytestmark
async def test_chats():
    chats = await functions.chats.get_chats_async(async_client)


@pytestmark
async def test_reports():
    report1 = await functions.reports.get_current_perfomance_async(
        async_client, os.environ["ASURSO_SID"]
    )
    report2 = await functions.reports.get_group_attestation_async(
        async_client, os.environ["ASURSO_SID"]
    )


# if __name__ == "__main__":
#     asyncio.run(main())
