from .exceptions import UnauthorizedError
from typing import TypeVar, List, Union, overload, Type
import hashlib
import logging
import base64
import httpx


logger = logging.getLogger(__name__)
T = TypeVar("T")


def hash_password(password: str) -> str:
    p1 = hashlib.sha256(password.encode()).digest()
    r = base64.b64encode(p1).decode()
    return r


@overload
def parse_response(r: httpx.Response, my_type: Type[T]) -> T: ...
@overload
def parse_response(r: httpx.Response, my_type: List[Type[T]]) -> List[T]: ...


def parse_response(
    r: httpx.Response,
    my_type: Union[Type[T], List[Type[T]]],
) -> Union[T, List[T]]:
    check_for_errors(r)
    data = r.json()
    logger.debug(f"{r.url=}, {data=}")

    if isinstance(my_type, list) and isinstance(my_type[0], type):
        return [my_type[0](**d) for d in data]

    elif isinstance(my_type, list):
        raise ValueError(
            f"You need to provide something like list[MyClass], not {my_type}..."
        )

    elif isinstance(my_type, (bool, float, int, str, list, tuple, set, dict)):
        result = data

    else:
        result = my_type(**data)
    return result


def check_for_errors(r: httpx.Response):
    if r.status_code == 401:
        d = r.json()
        if "responseStatus" not in d or "message" not in d["responseStatus"]:
            return
        raise UnauthorizedError(d["responseStatus"]["message"])
    return
    ...
