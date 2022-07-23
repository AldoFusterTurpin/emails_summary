from main import (
    convert_string_to_InfoSingleDepartment, InfoSingleDepartment, Report, 
    convert_list_of_strings_to_Report, get_target_lines, Summary, convert_summary_string_to_Summary
)
import pytest


@pytest.mark.parametrize(
    'input_data, expected_Report',
    [
        (
            [
                'GEOTRACKING 15h',
                'SPRINTS MALLS  75h',
                'SPRINTS 122h',
                'JIRA 108h',
                'matchings 53h',
                'formació i dubtes 82h',
                'Partnerships  1h',
                "OKR's 13h",
                'Coordinació 131.5h'
            ],
            Report(
                info_departments=[
                    InfoSingleDepartment("GEOTRACKING", 15),
                    InfoSingleDepartment("SPRINTS MALLS", 75),
                    InfoSingleDepartment("SPRINTS", 122),
                    InfoSingleDepartment("JIRA", 108),
                    InfoSingleDepartment("matchings", 53),
                    InfoSingleDepartment("formació i dubtes", 82),
                    InfoSingleDepartment("Partnerships", 1),
                    InfoSingleDepartment("OKR's", 13),
                    InfoSingleDepartment("Coordinació", 131.5)
                ],
                summary=None
            )
        )
    ]
)
def test_convert_lines_to_InfoDepartments(input_data, expected_Report):
    result = convert_list_of_strings_to_Report(input_data)
    assert expected_Report == result


@pytest.mark.parametrize(
    'input_data, expected_InfoSingle_Department',
    [
        ('GEOTRACKING 15h', InfoSingleDepartment("GEOTRACKING", 15)),
        ('SPRINTS MALLS  75h', InfoSingleDepartment("SPRINTS MALLS", 75)),
        ('SPRINTS 122h', InfoSingleDepartment("SPRINTS", 122)),
        ('JIRA 108h', InfoSingleDepartment("JIRA", 108)),
        ('matchings 53h', InfoSingleDepartment("matchings", 53)),
        ('formació i dubtes 82h', InfoSingleDepartment("formació i dubtes", 82)),
        ('Partnerships  1h', InfoSingleDepartment("Partnerships", 1)),
        ("OKR's 13h", InfoSingleDepartment("OKR's", 13)),
        ('Coordinació 131.5h', InfoSingleDepartment("Coordinació", 131.5)),
        ('   Prova prova interessant      80.5h', InfoSingleDepartment("Prova prova interessant", 80.5))
    ]
)
def test_convert_string_to_InfoSingleDepartment(input_data, expected_InfoSingle_Department):
    result = convert_string_to_InfoSingleDepartment(input_data)
    assert result == expected_InfoSingle_Department


@pytest.mark.parametrize(
    'input_data, expected_Summary',
    [
        ('600,5 hores efectives / 785.5 hores = 76% del total', Summary(600.5, 785.5, 76)),
        ('598 hores efectives / 800 hores = 74% del total', Summary(598, 800, 74)),
        ('666 hores efectives / 757 hores = 88% del total', Summary(666, 757, 88))
    ]
)
def test_convert_summary_line_to_Summary(input_data, expected_Summary):
    result = convert_summary_string_to_Summary(input_data)
    assert result == expected_Summary