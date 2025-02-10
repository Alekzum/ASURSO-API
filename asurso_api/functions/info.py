from typing import Protocol, List
from pydantic import BaseModel
import httpx


class TitleItem(BaseModel):
    language_code: str
    value: str


class LessonsMenu(BaseModel):
    isEnabled: bool
    sessionTableEnabled: bool
    examinationEnabled: bool
    profModuleExaminationEnabled: bool
    courseworksEnabled: bool


class EducationMenu(BaseModel):
    isEnabled: bool
    workingProgramsEnabled: bool


class UsersMenu(BaseModel):
    isEnabled: bool
    enrolleesEnabled: bool
    parentsEnabled: bool
    expelledStudentsEnabled: bool
    departmentsEnabled: bool


class ForeignInstallation(BaseModel):
    isEnabled: bool


class AvailableLanguage(BaseModel):
    key: str
    value: str


class Info(BaseModel):
    title: List[TitleItem]
    isFileStorageAvailable: bool
    isSupplementaryEducationCertificatesAvailable: bool
    isEditStudentFactualHoursAvailableForOrganization: bool
    isFactualHoursAvailableSystemwide: bool
    areChatsEnabled: bool
    isErnEnabled: bool
    isEmploymentEnabled: bool
    isReportsMenuEnabled: bool
    isPortfolioMenuEnabled: bool
    isAdministrationMenuEnabled: bool
    isOrgLicenseEnabled: bool
    isOrgDetailsEnabled: bool
    lessonsMenu: LessonsMenu
    educationMenu: EducationMenu
    usersMenu: UsersMenu
    foreignInstallation: ForeignInstallation
    defaultLanguage: str
    availableLanguages: List[AvailableLanguage]
    importEncoding: str


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


async def get_info_async(client: httpx.AsyncClient):
    r = await client.get("/services/people/system/info")
    data = r.json()
    return Info(**data)


def get_info_sync(client: httpx.Client):
    r = client.get("/services/people/system/info")
    data = r.json()
    return Info(**data)


class AsyncGetInfoMethod:
    async def get_info(self: AsyncASURSO):
        return await get_info_async(self._client)


class GetInfoMethod:
    def get_info(self: ASURSO):
        return get_info_sync(self._client)
