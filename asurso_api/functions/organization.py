from ..utils import parse_response
from pydantic import BaseModel, Field
from typing import Protocol
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


class Address(BaseModel):
    kladr: str
    mail_address: str = Field(..., alias="mailAddress")
    region: str
    settlement: str


class Attestation(BaseModel):
    is_enabled: bool = Field(..., alias="isEnabled")


class EService(BaseModel):
    cache_enrollee_list_timeout: int = Field(..., alias="cacheEnrolleeListTimeout")
    cache_enrollee_timeout: int = Field(..., alias="cacheEnrolleeTimeout")
    cache_specialty_list_timeout: int = Field(..., alias="cacheSpecialtyListTimeout")
    is_enabled: bool = Field(..., alias="isEnabled")
    url: str
    use_rest_integration: bool = Field(..., alias="useRestIntegration")


class FactHours(BaseModel):
    is_enabled: bool = Field(..., alias="isEnabled")


class VkChats(BaseModel):
    community_id: str = Field(..., alias="communityId")
    community_token: str = Field(..., alias="communityToken")


class Administration(BaseModel):
    attestation: Attestation
    e_service: EService = Field(..., alias="eService")
    fact_hours: FactHours = Field(..., alias="factHours")
    organization_id: str = Field(..., alias="organizationId")
    vk_chats: VkChats = Field(..., alias="vkChats")


class BankingDetails(BaseModel):
    founder_type: str = Field(..., alias="founderType")
    founders: str
    inn: str
    kpp: str
    ogrn: str
    okato: str
    okogu: str
    okopth: str
    okpo: str
    okths: str
    oktmo: str
    okved: str
    others: str


class Organization(BaseModel):
    abbreviation: str
    actual_address: str = Field(..., alias="actualAddress")
    additional_name: str = Field(..., alias="additionalName")
    address: Address
    administration: Administration
    banking_details: BankingDetails = Field(..., alias="bankingDetails")
    director_name: str = Field(..., alias="directorName")
    director_position: str = Field(..., alias="directorPosition")
    email: str
    entrepreneur_name: str = Field(..., alias="entrepreneurName")
    fax: str
    head_organization_name: str = Field(..., alias="headOrganizationName")
    is_entrepreneur_owned: bool = Field(..., alias="isEntrepreneurOwned")
    is_subdepartment: bool = Field(..., alias="isSubdepartment")
    legal_address: str = Field(..., alias="legalAddress")
    legal_status: str = Field(..., alias="legalStatus")
    name: str
    occupancy: int
    organization_dept_id: int = Field(..., alias="organizationDeptId")
    organization_id: str = Field(..., alias="organizationId")
    organization_status: str = Field(..., alias="organizationStatus")
    organization_type: str = Field(..., alias="organizationType")
    phone: str
    rosobr_id: str = Field(..., alias="rosobrId")
    shift_count: int = Field(..., alias="shiftCount")
    short_name: str = Field(..., alias="shortName")
    site: str
    study_unit_number: str = Field(..., alias="studyUnitNumber")
    type: str


async def get_organization_async(client: httpx.AsyncClient) -> Organization:
    r = await client.get("/services/people/organization")
    return parse_response(r, Organization)


def get_organization_sync(client: httpx.Client) -> Organization:
    r = client.get("/services/people/organization")
    return parse_response(r, Organization)


class AsyncGetOrganizationMethod:
    async def get_organization(self: AsyncASURSO):
        return await get_organization_async(self._client)


class GetOrganizationMethod:
    def get_organization(self: ASURSO):
        return get_organization_sync(self._client)
