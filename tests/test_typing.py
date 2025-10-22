from asurso_api import typing, classes


def test_async_asurso_type():
    assert all(
        x in classes.AsyncASURSO.__annotations__
        for x in typing.AsyncASURSO.__annotations__
    )


def test_asurso_type():
    assert all(
        x in classes.ASURSO.__annotations__ for x in typing.ASURSO.__annotations__
    )
