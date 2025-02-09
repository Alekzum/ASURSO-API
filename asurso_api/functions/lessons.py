from pydantic import BaseModel, Field
from typing import List, Optional, Protocol
import datetime
import httpx


class AsyncASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: httpx.AsyncClient


class ASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: httpx.Client


class Classroom(BaseModel):
    building: str
    name: str
    id: int


class Teacher(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: str = Field(..., alias="middleName")
    id: int


class Timetable(BaseModel):
    classroom: Classroom
    teacher: Teacher


class Task(BaseModel):
    id: int
    type: str
    topic: str
    condition: Optional[str] = None
    is_required: bool = Field(..., alias="isRequired")
    attachments: List
    mark: Optional[str] = None


class Gradebook(BaseModel):
    id: int
    themes: List[str]
    lesson_type: str = Field(..., alias="lessonType")
    tasks: List[Task]


class Lesson(BaseModel):
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    name: Optional[str] = None
    timetable: Optional[Timetable] = None
    gradebook: Optional[Gradebook] = None


class Day(BaseModel):
    date: str
    lessons: List[Lesson]
    is_holiday: bool = Field(..., alias="isHoliday")
    is_short: bool = Field(..., alias="isShort")


def format(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")


def resolve_edge(
    start: datetime.datetime | None = None,
    end: datetime.datetime | None = None,
    offset: int | None = None,
):
    if start is None:
        if (end is None) and (offset is None):
            start_ = datetime.datetime.now()
            end_ = start_ + datetime.timedelta(days=7)

        elif (end is None) and (offset is not None):
            start_ = datetime.datetime.now()
            end_ = start_ + datetime.timedelta(days=offset)

        elif (end is not None) and (offset is None):
            start_ = datetime.datetime.now()
            end_ = end

        elif (end is not None) and (offset is not None):
            start_ = end - datetime.timedelta(days=offset)
            end_ = end

    else:
        if (offset is None) and (end is None):
            start_ = start
            end_ = start + datetime.timedelta(days=7)

        elif (offset is None) and (end is not None):
            start_ = start
            end_ = end

        elif (offset is not None) and (end is None):
            start_ = start
            end_ = start + datetime.timedelta(days=offset)

        elif (offset is not None) and (end is not None):
            raise ValueError("Use only (start+end, start+offset, offset+end) pair")

    return start_, end_


async def get_lessons_async(
    client: httpx.AsyncClient,
    SID: str,
    start: datetime.datetime | None = None,
    end: datetime.datetime | None = None,
    offset: int | None = None,
) -> list[Day]:
    start_, end_ = resolve_edge(start, end, offset)

    r = await client.get(
        f"services/students/{SID}/lessons/{format(start_)}/{format(end_)}"
    )
    print(r, r.text)
    data = r.json()
    return [Day(**i) for i in data]


def get_lessons_sync(
    client: httpx.Client,
    SID: str,
    start: datetime.datetime | None = None,
    end: datetime.datetime | None = None,
    offset: int | None = None,
) -> list[Day]:
    start_, end_ = resolve_edge(start, end, offset)

    r = client.get(
        f"services/students/{SID}/lessons/{format(start_)}/{format(end_)}"
    )
    print(r, r.text)
    data = r.json()
    return [Day(**i) for i in data]


class AsyncGetLessonsMethod:
    async def get_lessons(
        self: AsyncASURSO,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        offset: int | None = None,
    ):
        return await get_lessons_async(
            self._client, self._SID, start=start, end=end, offset=offset
        )


class GetLessonsMethod:
    def get_lessons(
        self: ASURSO,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        offset: int | None = None,
    ):
        return get_lessons_sync(
            self._client, self._SID, start=start, end=end, offset=offset
        )
