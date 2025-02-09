import dotenv
import httpx
import sys
import os


sys.path.append(".")
dotenv.load_dotenv(".env")
from asurso_api import ASURSO, AsyncASURSO


async_client = httpx.AsyncClient(base_url="https://spo.asurso.ru")
sync_client = httpx.Client(base_url="https://spo.asurso.ru")

async_asurso = AsyncASURSO(
    login=os.environ["ASURSO-LOGIN"],
    password=os.environ["ASURSO-PASSWORD"],
    SID=os.environ["ASURSO-SID"],
)

sync_asurso = ASURSO(
    login=os.environ["ASURSO-LOGIN"],
    password=os.environ["ASURSO-PASSWORD"],
    SID=os.environ["ASURSO-SID"],
)
