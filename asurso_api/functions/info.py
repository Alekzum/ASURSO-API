from ..utils import parse_response, MyAsyncClient, MyClient
from typing import Protocol, List
from pydantic import BaseModel
import logging


logger = logging.getLogger(__name__)


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
    _client: MyAsyncClient


class ASURSO(Protocol):
    _SID: str
    _login: str
    _password: str
    _client: MyClient


async def get_info_async(client: MyAsyncClient) -> Info:
    r = await client.get("/services/people/system/info")
    return parse_response(r, Info)


def get_info_sync(client: MyClient) -> Info:
    r = client.get("/services/people/system/info")
    return parse_response(r, Info)


class AsyncGetInfoMethod:
    async def get_info(self: AsyncASURSO) -> Info:
        return await get_info_async(self._client)


class GetInfoMethod:
    def get_info(self: ASURSO) -> Info:
        return get_info_sync(self._client)
