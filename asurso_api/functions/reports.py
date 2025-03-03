from ..utils import parse_response
from typing import Any, Dict, List, Optional, Protocol
from pydantic import BaseModel, Field
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


# Current performance
class Month(BaseModel):
    num: int
    name: str


class MonthsWithDay(BaseModel):
    month: Month
    days_with_lessons: List[str] = Field(..., alias="daysWithLessons")


class DaysWithMark(BaseModel):
    day: str
    mark_values: List[str] = Field(..., alias="markValues")
    absence_type: Optional[str] = Field(None, alias="absenceType")


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


class Teacher(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: str = Field(..., alias="middleName")
    id: int


class Marks(BaseModel):
    field_21705: Dict[str, Any] = Field(..., alias="21705")


class Subject(BaseModel):
    examination_type: str = Field(..., alias="examinationType")
    teacher: Optional[Teacher] = None
    marks: Marks
    name: str
    id: int


class ProfModule(BaseModel):
    marks: Dict[str, Any]
    name: str
    id: int


class Marks1(BaseModel):
    field_21705: Dict[str, Any] = Field(..., alias="21705")


class CourseWork(BaseModel):
    marks: Marks1
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


async def get_current_performance_async(
    client: httpx.AsyncClient, SID: str
) -> CurrentPerformance:
    r = await client.get(f"/services/reports/current/performance/{SID}")
    return parse_response(r, CurrentPerformance)
    data = r.json()
    return CurrentPerformance(**data)


async def get_group_attestation_async(
    client: httpx.AsyncClient, SID: str
) -> GroupAttestation:
    r = await client.get(
        f"/services/reports/curator/group-attestation-for-student/{SID}"
    )
    data = r.json()
    return GroupAttestation(**data)


def get_current_performance_sync(client: httpx.Client, SID: str) -> CurrentPerformance:
    r = client.get(f"/services/reports/current/performance/{SID}")
    data = r.json()
    return CurrentPerformance(**data)


def get_group_attestation_sync(client: httpx.Client, SID: str) -> GroupAttestation:
    r = client.get(f"/services/reports/curator/group-attestation-for-student/{SID}")
    data = r.json()
    return GroupAttestation(**data)


class AsyncGetReportMethods:
    async def get_current_performance(self: AsyncASURSO):
        return await get_current_performance_async(self._client, self._SID)

    async def get_group_attestation(self: AsyncASURSO):
        return await get_group_attestation_async(self._client, self._SID)


class GetReportMethods:
    def get_current_performance(self: ASURSO):
        return get_current_performance_sync(self._client, self._SID)

    def get_group_attestation(self: ASURSO):
        return get_group_attestation_sync(self._client, self._SID)
