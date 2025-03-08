from .. import enums
from ..utils import parse_response, MyAsyncClient, MyClient
from typing import Any, Dict, List, Optional, Protocol, Union
from pydantic import BaseModel, Field, computed_field
import datetime


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


# Current performance
class MonthsWithDay(BaseModel):
    raw_month: dict = Field(..., alias="month")
    raw_days_with_lessons: List[str] = Field(..., alias="daysWithLessons")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def days_with_lessons(self) -> List[datetime.date]:
        return [
            datetime.date.fromisoformat(d.split("T")[0])
            for d in self.raw_days_with_lessons
        ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def month(self) -> int:
        return self.raw_month["num"] - 1


class DaysWithMark(BaseModel):
    raw_day: str = Field(..., alias="day")
    mark_values: List[enums.MarkValue] = Field(..., alias="markValues")
    absence_type: Optional[enums.AbsenceType] = Field(None, alias="absenceType")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mark(self) -> str:
        return mark_to_text(self.absence_type) if self.absence_type else ", ".join([mark_to_text(i) for i in self.mark_values])

    @computed_field  # type: ignore[prop-decorator]
    @property
    def day(self) -> datetime.date:
        return datetime.date.fromisoformat(self.raw_day.split("T")[0])


class DaysWithMarksForSubjectItem(BaseModel):
    subject_name: str = Field(..., alias="subjectName")
    days_with_marks: List[DaysWithMark] = Field(..., alias="daysWithMarks")
    average_mark: Optional[float] = Field(None, alias="averageMark")


class CurrentPerformance(BaseModel):
    months_with_days: List[MonthsWithDay] = Field(..., alias="monthsWithDays")
    days_with_marks_for_subject: List[DaysWithMarksForSubjectItem] = Field(
        ..., alias="daysWithMarksForSubject"
    )


# Group attestation
class Student(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: str = Field(..., alias="middleName")
    id: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def full_name(self) -> str:
        return " ".join([self.last_name, self.first_name, self.middle_name])


class Teacher(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: str = Field(..., alias="middleName")
    id: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def full_name(self) -> str:
        return " ".join([self.last_name, self.first_name, self.middle_name])


class Subject(BaseModel):
    examination_type: enums.ExaminationType = Field(..., alias="examinationType")
    teacher: Optional[Teacher] = None
    marks: Dict[str, Any]
    name: str
    id: int


class ProfModule(BaseModel):
    marks: Dict[str, Any]
    name: str
    id: int


class CourseWork(BaseModel):
    marks: Dict[str, Any]
    name: str
    id: int


class GroupAttestation(BaseModel):
    term_type: str = Field(..., alias="termType")
    term_number: int = Field(..., alias="termNumber")
    year: int
    students: List[Student]
    subjects: List[Subject]
    prof_modules: List[ProfModule] = Field(..., alias="profModules")
    course_works: List[CourseWork] = Field(..., alias="courseWorks")
    department_name: str = Field(..., alias="departmentName")


def mark_to_text(obj: Union[enums.MarkValue, enums.AbsenceType]) -> str:
    return {
        enums.MarkValue.FIVE: "5",
        enums.MarkValue.FOUR: "4",
        enums.MarkValue.THREE: "3",
        enums.MarkValue.TWO: "2",
        enums.AbsenceType.IS_ABSENT_BY_NOT_VALID_REASON: "нп",
        enums.AbsenceType.IS_ABSENT_BY_VALID_REASON: "уп",
        enums.AbsenceType.IS_LATE: "оп",
        enums.AbsenceType.SICK_LEAVE: "б"
    }[obj]


async def get_current_performance_async(client: MyAsyncClient) -> CurrentPerformance:
    r = await client.get(f"/services/reports/current/performance/{client._SID}")
    return parse_response(r, CurrentPerformance)


async def get_group_attestation_async(client: MyAsyncClient) -> GroupAttestation:
    r = await client.get(
        f"/services/reports/curator/group-attestation-for-student/{client._SID}"
    )
    return parse_response(r, GroupAttestation)


def get_current_performance_sync(client: MyClient) -> CurrentPerformance:
    r = client.get(f"/services/reports/current/performance/{client._SID}")
    return parse_response(r, CurrentPerformance)


def get_group_attestation_sync(client: MyClient) -> GroupAttestation:
    r = client.get(
        f"/services/reports/curator/group-attestation-for-student/{client._SID}"
    )
    return parse_response(r, GroupAttestation)


class AsyncGetReportMethods:
    async def get_current_performance(self: AsyncASURSO):
        return await get_current_performance_async(self._client)

    async def get_group_attestation(self: AsyncASURSO):
        return await get_group_attestation_async(self._client)


class GetReportMethods:
    def get_current_performance(self: ASURSO):
        return get_current_performance_sync(self._client)

    def get_group_attestation(self: ASURSO):
        return get_group_attestation_sync(self._client)
