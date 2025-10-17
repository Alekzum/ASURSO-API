from . import get_test_data, mark_test_class
from asurso_api import classes
import datetime


@mark_test_class
def test_login():
    login_info_raw = get_test_data("login")
    login_info = classes.LoginInfo.model_validate(login_info_raw)
    
    assert isinstance(login_info.tenant_name, str)
    assert isinstance(login_info.tenants[login_info.tenant_name], classes.login.Spo)


@mark_test_class
def test_attestation():
    attestation_raw = get_test_data("attestation")
    attestation = classes.Attestation.model_validate(attestation_raw)

    for year in attestation.academic_years or []:
        assert isinstance(year, classes.attestation.AcademicYear)
        for term in year.terms:
            assert isinstance(term, classes.attestation.Term)
            break
        break


@mark_test_class
def test_chats():
    chats = get_test_data("chats")
    for chat in chats:
        classes.Chat.model_validate(chat)


@mark_test_class
def test_current_performance():
    current_performance_raw = get_test_data("report_current_performance")
    current_performance = classes.CurrentPerformance.model_validate(current_performance_raw)

    for days in current_performance.days_with_marks_for_subject:
        for day in days.days_with_marks:
            assert isinstance(day.day, datetime.date)
            assert isinstance(day.mark, str)


@mark_test_class
def test_dashboard():
    dashboard_raw = get_test_data("dashboard")
    dashboard = classes.Dashboard.model_validate(dashboard_raw)


@mark_test_class
def test_group_attestation():
    group_attestation_raw = get_test_data("report_group_attestation")
    group_attestation = classes.GroupAttestation.model_validate(group_attestation_raw)


@mark_test_class
def test_info():
    info_raw = get_test_data("info")
    classes.Info.model_validate(info_raw)


@mark_test_class
def test_lessons():
    lessons_raw = get_test_data("lessons")
    
    for lesson_raw in lessons_raw:
        lesson = classes.LessonsDay.model_validate(lesson_raw)
        assert isinstance(lesson.date, datetime.date)


@mark_test_class
def test_organization():
    organization_raw = get_test_data("organization")
    organization = classes.Organization.model_validate(organization_raw)
