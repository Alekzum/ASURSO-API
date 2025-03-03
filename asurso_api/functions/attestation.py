from ..utils import parse_response
from typing import List, Optional, Protocol
from pydantic import BaseModel, Field
import logging
import httpx


logger = logging.getLogger(__name__)


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


class Term(BaseModel):
    id: int
    is_active: bool = Field(..., alias="isActive")
    number: int


class AcademicYear(BaseModel):
    id: int
    number: int
    term_type: str = Field(..., alias="termType")
    terms: List[Term]


class FinalMark(BaseModel):
    value: Optional[str] = None


class FieldMark(BaseModel):
    value: Optional[str] = None


class Marks(BaseModel):
    field: Optional[FieldMark] = Field(None, pattern=r"^\d$")


class Subject(BaseModel):
    final_mark: Optional[FinalMark] = Field(default=None, alias="finalMark")
    marks: Optional[Marks] = None
    name: str


class Attestation(BaseModel):
    academic_years: Optional[List[AcademicYear]] = Field(None, alias="academicYears")
    subjects: List[Subject]


async def get_attestation_async(client: httpx.AsyncClient, SID: str) -> Attestation:
    r = await client.get(f"services/students/{SID}/dashboard")
    return parse_response(r, Attestation)


def get_attestation_sync(client: httpx.Client, SID: str) -> Attestation:
    r = client.get(f"services/students/{SID}/dashboard")
    return parse_response(r, Attestation)


class AsyncGetAttestationMethod:
    async def get_attestation(self: AsyncASURSO) -> Attestation:
        return await get_attestation_async(self._client, self._SID)


class GetAttestationMethod:
    def get_attestation(self: ASURSO) -> Attestation:
        return get_attestation_sync(self._client, self._SID)
