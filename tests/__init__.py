from asurso_api import ASURSO, AsyncASURSO
import dotenv
import pytest
import httpx
import os


dotenv.load_dotenv(".env")


pytestmark = pytest.mark.asyncio(loop_scope="session")
async_client = httpx.AsyncClient(base_url="https://spo.asurso.ru")
sync_client = httpx.Client(base_url="https://spo.asurso.ru")

async_asurso = AsyncASURSO(
    login=os.environ["ASURSO_LOGIN"],
    password=os.environ["ASURSO_PASSWORD"],
    SID=os.environ["ASURSO_SID"],
)

sync_asurso = ASURSO(
    login=os.environ["ASURSO_LOGIN"],
    password=os.environ["ASURSO_PASSWORD"],
    SID=os.environ["ASURSO_SID"],
)
