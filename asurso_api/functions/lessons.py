from typing import List, Optional, Protocol, Union, Tuple
from pydantic import BaseModel, Field
from ..enums import LessonsPeriod
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

    def humanize(self):
        return f"<Кабинет {self.name} в корпусе {self.building}>"


class Teacher(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: str = Field(..., alias="middleName")
    id: int

    def humanize(self):
        return f"<Преподаватель {self.last_name} {self.first_name} {self.middle_name}>"


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

    @property
    def ru_type(self):
        if self.type == "Home":
            return "Домашняя работа"
        return self.type

    def humanize(self):
        add_info: "list[str]" = []
        if self.is_required:
            add_info.append("обязательная")
        else:
            add_info.append("не обязательная")
        add_info.append(f"{self.topic!r}")

        if self.condition:
            add_info.append(f"с условием {self.condition}")
        if self.attachments:
            add_info.append(f"с прикреплениями: {self.attachments}")
        if self.mark:
            add_info.append(f"с оценкой {self.mark!r}")

        add_info_str = ", ".join([""] + add_info) if add_info else ""
        return f"<{self.ru_type}{add_info_str}>"


class Gradebook(BaseModel):
    id: int
    themes: List[str]
    lesson_type: str = Field(..., alias="lessonType")
    tasks: List[Task]

    @property
    def ru_lesson_type(self):
        if self.lesson_type == "Lesson":
            return "Лекция"
        elif self.lesson_type == "PracticalTraining":
            return "Практическая работа"
        return self.lesson_type

    def humanize(self, themes=True):
        add_info: "list[str]" = []
        if themes:
            add_info.append(f"по темам ({', '.join([repr(t) for t in self.themes])})")

        add_info_str = ", ".join([""] + add_info) if add_info else ""

        return f"<{self.ru_lesson_type}{add_info_str}: ({', '.join([t.humanize() for t in self.tasks]) or 'без задач'})>"


class Lesson(BaseModel):
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    name: Optional[str] = None
    timetable: Optional[Timetable] = None
    gradebook: Optional[Gradebook] = None

    def humanize(self):
        additional_info = []
        timetable = self.timetable
        if timetable:
            classroom = timetable.classroom
            additional_info.append(f"в кабинете {classroom.name}")

        gradebook = self.gradebook
        if gradebook:
            additional_info.append(f"с заданием ({gradebook.humanize()})")

        add_info = ", ".join([""] + additional_info) if additional_info else ""
        return f"<Пара с {self.start_time} - {self.end_time}: {self.name or '*неизвестно*'}{add_info}>"


class LessonsDay(BaseModel):
    date_raw: str = Field("", validation_alias="date")
    lessons: List[Lesson]
    is_holiday: bool = Field(..., alias="isHoliday")
    is_short: bool = Field(..., alias="isShort")

    @property
    def date(self):
        if hasattr(self, "_d"):
            return getattr(self, "_d")
        _d = datetime.datetime.strptime(self.date_raw.split("T")[0], "%Y-%m-%d")
        setattr(self, "_d", _d)
        return _d

    @property
    def ru_date(self):
        return format(self.date, rus=True)

    def humanize(self):
        return f"<Занятия на {self.date:%d.%m.%y}: {', '.join([lesson.humanize() for lesson in self.lessons])}>"


def format(date: Union[datetime.date, datetime.datetime], rus=False) -> str:
    if rus:
        return date.strftime("%d.%m.%Y")
    return date.strftime("%Y-%m-%d")


def resolve_edge(
    start: Optional[Union[datetime.date, datetime.datetime, LessonsPeriod]] = None,
    end: Optional[Union[datetime.date, datetime.datetime]] = None,
    offset: Optional[int] = None,
) -> Tuple[datetime.date, datetime.date]:
    cur = datetime.datetime.now()
    if isinstance(start, datetime.date):
        start = datetime.datetime.combine(start, cur.time())

    if isinstance(end, datetime.date):
        end = datetime.datetime.combine(end, cur.time())

    for_enum: dict[LessonsPeriod, tuple[datetime.datetime, datetime.datetime]] = {
        # days
        LessonsPeriod.PREVIOUS_DAY: (
            cur - datetime.timedelta(days=1),
            cur - datetime.timedelta(days=1),
        ),
        LessonsPeriod.TODAY: (cur, cur),
        LessonsPeriod.NEXT_DAY: (
            cur + datetime.timedelta(days=1),
            cur + datetime.timedelta(days=1),
        ),
        # weeks
        LessonsPeriod.PREVIOUS_WEEK: (
            cur - datetime.timedelta(days=cur.weekday(), weeks=1),
            cur - datetime.timedelta(days=cur.weekday() - 6, weeks=1),
        ),
        LessonsPeriod.THIS_WEEK: (
            cur - datetime.timedelta(days=cur.weekday()),
            cur - datetime.timedelta(days=cur.weekday() - 6),
        ),
        LessonsPeriod.NEXT_WEEK: (
            cur - datetime.timedelta(days=cur.weekday(), weeks=-1),
            cur - datetime.timedelta(days=cur.weekday() - 6, weeks=-1),
        ),
        # months
        LessonsPeriod.PREVIOUS_MONTH: (
            datetime.datetime(cur.year, cur.month - 1, 1),
            datetime.datetime(cur.year, cur.month, 1) - datetime.timedelta(days=1),
        ),
        LessonsPeriod.THIS_MONTH: (
            datetime.datetime(cur.year, cur.month, 1),
            datetime.datetime(cur.year, cur.month + 1, 1) - datetime.timedelta(days=1),
        ),
        LessonsPeriod.NEXT_MONTH: (
            datetime.datetime(cur.year, cur.month + 1, 1),
            datetime.datetime(cur.year, cur.month + 2, 1) - datetime.timedelta(days=1),
        ),
    }

    if isinstance(start, LessonsPeriod):
        return for_enum[start][0].date(), for_enum[start][1].date()

    if start is None:
        if offset is None and end is None:
            return (cur.date(), (cur + datetime.timedelta(days=7)).date())
        elif offset is None and end is not None:
            return (cur.date(), end.date())
        elif offset is not None and end is None:
            return (cur.date(), (cur + datetime.timedelta(days=offset)).date())

        assert offset is not None and end is not None
        return ((end - datetime.timedelta(days=offset)).date(), end.date())

    assert start is not None
    if offset is None and end is None:
        return (start.date(), (start + datetime.timedelta(days=7)).date())
    elif offset is None and end is not None:
        return (start.date(), end.date())
    elif offset is not None and end is None:
        return (start.date(), (start + datetime.timedelta(days=offset)))

    assert end is not None and offset is not None
    raise ValueError("Use only (start+end, start+offset, offset+end) pair")
    # temp_result = pairs[start is None][(end is None and offset is None)]
    # if isinstance(temp_result, Exception):
    #     raise temp_result
    # return

    # if (offset is None) and (end is None):
    #     return

    # elif (offset is None) and (end is not None):
    #     return

    # elif (offset is not None) and (end is None):
    #     return

    # elif (offset is not None) and (end is not None):
    raise ValueError("Use only (start+end, start+offset, offset+end) pair")


async def get_lessons_async(
    client: httpx.AsyncClient,
    SID: str,
    start: Union[datetime.date, datetime.datetime, LessonsPeriod] = LessonsPeriod.THIS_WEEK,
    end: Optional[Union[datetime.date, datetime.datetime]] = None,
    offset: Optional[int] = None,
) -> List[LessonsDay]:
    start_, end_ = resolve_edge(start, end, offset)

    r = await client.get(
        f"services/students/{SID}/lessons/{format(start_, rus=False)}/{format(end_, rus=False)}"
    )
    print(r, r.text)
    data = r.json()
    return [LessonsDay(**i) for i in data]


def get_lessons_sync(
    client: httpx.Client,
    SID: str,
    start: Union[datetime.date, datetime.datetime, LessonsPeriod] = LessonsPeriod.THIS_WEEK,
    end: Optional[Union[datetime.date, datetime.datetime]] = None,
    offset: Optional[int] = None,
) -> List[LessonsDay]:
    start_, end_ = resolve_edge(start, end, offset)

    r = client.get(
        f"services/students/{SID}/lessons/{format(start_, rus=False)}/{format(end_, rus=False)}"
    )
    data = r.json()
    return [LessonsDay(**i) for i in data]


class AsyncGetLessonsMethod:
    async def get_lessons(
        self: AsyncASURSO,
        start: Union[datetime.date, datetime.datetime, LessonsPeriod] = LessonsPeriod.THIS_WEEK,
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
        offset: Optional[int] = None,
    ):
        return await get_lessons_async(
            self._client, self._SID, start=start, end=end, offset=offset
        )


class GetLessonsMethod:
    def get_lessons(
        self: ASURSO,
        start: Union[datetime.date, datetime.datetime, LessonsPeriod] = LessonsPeriod.THIS_WEEK,
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
        offset: Optional[int] = None,
    ):
        return get_lessons_sync(
            self._client, self._SID, start=start, end=end, offset=offset
        )
