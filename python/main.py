# ALDO FUSTER TURPIN

from pathlib import Path, PosixPath
from dataclasses import dataclass, field
from email import policy
from email.parser import BytesParser
from typing import Tuple
import csv
import os

HOURS_SUMMARY = "Resum hores:"
THANKS = "Gràcies!"
EFFECTIVE_HOURS = "hores efectives"
HOURS = "hores"
FROM_TOTAL = "del total"
STORES_SUMMARY = "Resum tiendas"

FILE_SUFIX = ".eml"

IN_FOLDER = "input_files"
OUT_FOLDER = "results"
DEPARTMENTS_FILE = "departments.csv"
SUMMARY_FILE = "summary.csv"

CSV_DELIMITER = ","
QUOTECHAR = '"'


@dataclass
class InfoSingleDepartment:
    department_name: str
    hours: float


@dataclass
class Summary:
    effective_hours: float
    total_hours: float
    percentage_effective_hours_to_total: float


@dataclass
class Report:
    info_departments: list[InfoSingleDepartment] = field(default_factory=list)
    summary: Summary = None
    the_date: str = None


def get_input_paths()-> list[PosixPath]:
    p = Path().cwd() / IN_FOLDER
    eml_paths = [child for child in p.iterdir()]

    return eml_paths


def get_content_of_eml_file_as_string_and_file_name(file: PosixPath) -> (str, str):
    with open(file, 'rb') as f:
            parser = BytesParser(policy=policy.default)
            message_structure = parser.parse(f)
            text = message_structure.get_body(preferencelist=('plain')).get_content()
            print("Analysing file ", f.name)

            p = Path(f.name)
            path_parts = p.parts
            file_name = path_parts[-1]

            return text, file_name


def clean_line(line: str)-> str:
    line = line.strip()

    if line == "":
        return None

    if line.startswith(">"):
        line = line[1:].strip()
        if line == "":
            return None

    return line


def get_target_lines(file_content: str) -> list[str]:
    first_split_token = HOURS_SUMMARY

    _, after = file_content.split(first_split_token)

    second_split_token = THANKS
    target, _ = after.split(second_split_token)

    target_splitted_lines = target.split(os.linesep)

    res = []
    for line in target_splitted_lines:
        res_line = clean_line(line)

        if res_line is not None:
            res.append(res_line)

    return res


# convert_string_to_InfoSingleDepartment() converts a line like
# 'GEOTRACKING 15h'
# to the corresponding InfoSingleDepartment object
def convert_string_to_InfoSingleDepartment(line: str) -> InfoSingleDepartment:
    line_splitted = line.rsplit(" ", 1)

    department_name, hours = line_splitted[0], line_splitted[1]

    department_name = department_name.strip()
    hours = float(
        hours[:-1] # remove the 'h' character
        .strip().replace(",", ".") # to ensure float() conversion works
    )

    return InfoSingleDepartment(department_name, hours)


def convert_list_of_strings_to_Report(lines: list[str])-> Report:
    report = Report()

    report.info_departments = [convert_string_to_InfoSingleDepartment(line) for line in lines]
    return report


def clean_summary_line(summary_line: str):
    summary_line = summary_line.strip()
    summary_line = summary_line.replace("*", "")
    return summary_line


def get_effective_hours_from_effective_hours_part(effective_hours_part: str) -> float:
    effective_hours_part = effective_hours_part.strip()
    effective_hours_part_splitted = effective_hours_part.split(EFFECTIVE_HOURS)
    effective_hours = effective_hours_part_splitted[0]
    effective_hours = effective_hours.strip()
    effective_hours = effective_hours.replace(",", ".")
    return float(effective_hours)

def get_total_hours_from_total_hours_part(total_hours_part: str) -> float:
    total_hours_part = total_hours_part.strip()
    total_hours_part_splitted = total_hours_part.split(HOURS)
    total_hours = total_hours_part_splitted[0]
    total_hours = total_hours.strip()
    total_hours = total_hours.replace(",", ".")
    return float(total_hours)


def get_percentage_effective_hours_to_total_from_percentage_effective_hours_to_total_part(percentage_effective_hours_to_total_part: str) -> float:
    percentage_effective_hours_to_total_part = percentage_effective_hours_to_total_part.strip()
    percentage_effective_hours_to_total_splitted = percentage_effective_hours_to_total_part.split(FROM_TOTAL)
    percentage_effective_hours_to_total = percentage_effective_hours_to_total_splitted[0]
    percentage_effective_hours_to_total = percentage_effective_hours_to_total.strip()
    percentage_effective_hours_to_total = percentage_effective_hours_to_total.replace("%", "")
    percentage_effective_hours_to_total = percentage_effective_hours_to_total.replace(",", ".")
    return float(percentage_effective_hours_to_total)


def convert_summary_string_to_Summary(line: str):
    splitted_line = line.split("=")
    left_part = splitted_line[0]
    percentage_effective_hours_to_total_part = splitted_line[1]

    left_part_splitted = left_part.split("/")
    effective_hours_part = left_part_splitted[0]
    total_hours_part = left_part_splitted[1]

    effective_hours = get_effective_hours_from_effective_hours_part(effective_hours_part)
    total_hours = get_total_hours_from_total_hours_part(total_hours_part)
    percentage_effective_hours_to_total = get_percentage_effective_hours_to_total_from_percentage_effective_hours_to_total_part(percentage_effective_hours_to_total_part)

    return Summary(effective_hours, total_hours, percentage_effective_hours_to_total)


def process_single_file(file_content: str) -> list[Report]:
    target_lines = get_target_lines(file_content)

    summary_string = target_lines[-1]
    summary_string = clean_summary_line(summary_string)
    summary = convert_summary_string_to_Summary(summary_string)

    report = convert_list_of_strings_to_Report(target_lines[:-1])
    report.summary = summary

    return report


def get_Reports_from(input_paths: list[PosixPath]) -> list[Report]:
    reports: list[Report] = []

    for file in input_paths:
        file_content, file_name = get_content_of_eml_file_as_string_and_file_name(file)
        
        if file_name.startswith("."):
            continue
        
        report = process_single_file(file_content)

        the_date = file_name.replace(FILE_SUFIX, "").replace(STORES_SUMMARY, "").strip().replace(" ", "_")
        report.the_date = the_date

        reports.append(report)

    return reports


def is_info_department_in_csv(info_department_date: str, info_department_name: str, departments_file_path_output):
    csv_reader_report = csv.reader(open(str(departments_file_path_output), "r"), delimiter=CSV_DELIMITER)

    for csv_row in csv_reader_report:

        #skip blank lines
        if len(csv_row) == 0:
            continue

        info_department_date_in_csv = csv_row[0]
        info_department_name_in_csv = csv_row[1]
        if info_department_date_in_csv + info_department_name_in_csv == info_department_date + info_department_name:
            return True

    return False


def is_report_summary_in_csv(summary_date: str, summary_file_path):
    csv_summary_report = csv.reader(open(str(summary_file_path), "r"), delimiter=CSV_DELIMITER)

    for csv_row in csv_summary_report: 
        #skip blank lines
        if len(csv_row) == 0:
            continue

        summary_date_in_csv = csv_row[0]
        if summary_date_in_csv == summary_date:
            return True

    return False


def write_report_to_csv(report, departments_file_path_output, csv_writer):
    for department in report.info_departments:
        report_date = report.the_date
        department_name = department.department_name
        
        if not is_info_department_in_csv(str(report_date), str(department_name), departments_file_path_output):
            row_to_write = [report_date, department_name, department.hours]
            csv_writer.writerow(row_to_write)


def write_report_summary_to_csv(date: str, summary: Summary, summary_file_path: Path, csv_writer):
    if not is_report_summary_in_csv(str(date), summary_file_path):
        row_to_write = [date, summary.effective_hours, summary.total_hours, summary.percentage_effective_hours_to_total]
        csv_writer.writerow(row_to_write)


def write_data_to_csv(reports: list[Report], departments_file_path_output: Path, summary_file_path_output: Path):
    departments_file_path_output.parent.mkdir(parents=True, exist_ok=True)
    summary_file_path_output.parent.mkdir(parents=True, exist_ok=True)

    with open(departments_file_path_output, mode='a') as f:
        with open(summary_file_path_output, mode='a') as f2:
            csv_report_writer = csv.writer(f, delimiter=CSV_DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
            csv_summary_writer = csv.writer(f2, delimiter=CSV_DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)

            for report in reports:
                write_report_to_csv(report, departments_file_path_output, csv_report_writer)
                write_report_summary_to_csv(report.the_date, report.summary, summary_file_path_output, csv_summary_writer)


def main():
    input_paths = get_input_paths()
    reports_from_input_files = get_Reports_from(input_paths)
    
    departments_file_path_output = Path().cwd() / OUT_FOLDER / DEPARTMENTS_FILE
    summary_file_path_output = Path().cwd() / OUT_FOLDER / SUMMARY_FILE

    write_data_to_csv(reports_from_input_files, departments_file_path_output, summary_file_path_output)


if __name__ == "__main__":
    main()
