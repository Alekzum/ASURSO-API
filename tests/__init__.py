from asurso_api import ASURSO, AsyncASURSO
import dotenv
import pytest
import httpx
import os


dotenv.load_dotenv(".env")


pytestmark = pytest.mark.asyncio(loop_scope="session")
async_client = httpx.AsyncClient(base_url="https://spo.asurso.ru", timeout=30)
sync_client = httpx.Client(base_url="https://spo.asurso.ru", timeout=30)
env = os.environ

async_asurso = AsyncASURSO(
    login=env["ASURSO_LOGIN"],
    password=env["ASURSO_PASSWORD"],
    timeout=30,
)

sync_asurso = ASURSO(
    login=env["ASURSO_LOGIN"],
    password=env["ASURSO_PASSWORD"],
    timeout=30,
)
