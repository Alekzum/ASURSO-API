from ..utils import parse_response, MyAsyncClient, MyClient, range_to_dates
from typing import (
    List,
    Optional,
    Protocol,
    Union,
    TypeVar,
    Type,
    cast,
)
from pydantic import BaseModel, Field, computed_field
from .. import enums
import datetime
import logging


logger = logging.getLogger(__name__)
T = TypeVar("T", datetime.datetime, None)


class AsyncASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: MyAsyncClient


class ASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: MyClient


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

    @computed_field
    @property
    def full_name(self) -> str:
        return " ".join([self.last_name, self.first_name, self.middle_name])

    def humanize(self):
        return f"<Преподаватель {self.full_name}>"


class Timetable(BaseModel):
    classroom: Classroom
    teacher: Teacher


class Task(BaseModel):
    id: int
    type: enums.EducationTaskType
    topic: str
    condition: Optional[str] = None
    is_required: bool = Field(..., alias="isRequired")
    attachments: List
    mark: Optional[str] = None

    @property
    def ru_type(self) -> str:
        if self.type == enums.EducationTaskType.HOME:
            return "Домашняя работа"
        return self.type.name.title().replace("_", "")

    def humanize(self):
        add_info = []
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
        add_info = []
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

    @computed_field
    @property
    def date(self) -> datetime.date:
        _d = datetime.date.fromisoformat(self.date_raw.split("T")[0])
        return _d

    @property
    def ru_date(self) -> str:
        """something like "01.01.2021" """
        return format(self.date, rus=True)

    def humanize(self):
        return f"<Занятия на {self.ru_date}: {', '.join([lesson.humanize() for lesson in self.lessons])}>"


def format(date: Union[datetime.date, datetime.datetime], rus=False) -> str:
    if rus:
        return date.strftime("%d.%m.%Y")
    return date.strftime("%Y-%m-%d")


async def get_lessons_async(
    client: MyAsyncClient,
    start: Union[
        datetime.date, datetime.datetime, enums.LessonsPeriod
    ] = enums.LessonsPeriod.THIS_WEEK,
    end: Optional[Union[datetime.date, datetime.datetime]] = None,
    offset: Optional[int] = None,
) -> List[LessonsDay]:
    start_, end_ = range_to_dates(start, end, offset)

    r = await client.get(
        f"services/students/{client._SID}/lessons/{format(start_, rus=False)}/{format(end_, rus=False)}"
    )
    return parse_response(r, [LessonsDay])


def get_lessons_sync(
    client: MyClient,
    start: Union[
        datetime.date, datetime.datetime, enums.LessonsPeriod
    ] = enums.LessonsPeriod.THIS_WEEK,
    end: Optional[Union[datetime.date, datetime.datetime]] = None,
    offset: Optional[int] = None,
) -> List[LessonsDay]:
    start_, end_ = range_to_dates(start, end, offset)

    r = client.get(
        f"services/students/{client._SID}/lessons/{format(start_, rus=False)}/{format(end_, rus=False)}"
    )
    return parse_response(r, [LessonsDay])


class AsyncGetLessonsMethod:
    async def get_lessons(
        self: AsyncASURSO,
        start: Union[
            datetime.date, datetime.datetime, enums.LessonsPeriod
        ] = enums.LessonsPeriod.THIS_WEEK,
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
        offset: Optional[int] = None,
    ):
        return await get_lessons_async(
            self._client, start=start, end=end, offset=offset
        )


class GetLessonsMethod:
    def get_lessons(
        self: ASURSO,
        start: Union[
            datetime.date, datetime.datetime, enums.LessonsPeriod
        ] = enums.LessonsPeriod.THIS_WEEK,
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
        offset: Optional[int] = None,
    ):
        return get_lessons_sync(
            self._client, start=start, end=end, offset=offset
        )
