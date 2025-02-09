from . import sync_asurso, ASURSO


def test_login():
    sync_asurso.login()


def test_attestation():
    sync_asurso.get_attestation()


def test_chats():
    sync_asurso.get_chats()


def test_current_perfomance():
    sync_asurso.get_current_perfomance()


def test_dashboard():
    sync_asurso.get_dashboard()


def test_group_attestation():
    sync_asurso.get_group_attestation()


def test_info():
    sync_asurso.get_info()


def test_lessons():
    sync_asurso.get_lessons()


def test_organization():
    sync_asurso.get_organization()


def test_logout():
    sync_asurso.logout()


def test_context():
    with sync_asurso as syns_asurso2:
        syns_asurso2.get_info()