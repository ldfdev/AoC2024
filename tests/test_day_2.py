from pathlib import Path
from aoc import day2

day_2_file: Path = Path(__file__).parent / "day2.input"


def test_is_report_safe():
    report: day2.Report = [7, 6, 4, 2, 1]
    assert day2.is_report_safe(report) is True

    report: day2.Report = [1, 2, 7, 8, 9]
    # not safe becasue between 2, 7 there is a diff of 5
    assert day2.is_report_safe(report) is False

    report: day2.Report = [9, 7, 6, 2, 1]
    # not safe becasue between 6, 2 there is a diff of 4
    assert day2.is_report_safe(report) is False

    report: day2.Report = [1, 3, 2, 4, 5]
    # not safe becasue between the sequence is not strictly increasing or strictly decreasing
    assert day2.is_report_safe(report) is False

    report: day2.Report = [8, 6, 4, 4, 1]
    # not safe becasue between the sequence is not strictly increasing or strictly decreasing
    # 4, 4 is constant
    assert day2.is_report_safe(report) is False

    report: day2.Report = [1, 3, 6, 7, 9]
    assert day2.is_report_safe(report) is True


def test_get_safe_reports():
    reports: day2.Reports = day2.read_reports_from_file(day_2_file)
    assert day2.get_safe_reports(reports) == 2


def test_is_report_unsafe_by_single_bad_level():
    report: day2.Report = [7, 6, 4, 2, 1]
    # this report is safe
    assert day2.is_report_unsafe_by_single_bad_level(report) is False

    report: day2.Report = [1, 2, 7, 8, 9]
    # not safe becasue between 2, 7 there is a diff of 5
    assert day2.is_report_unsafe_by_single_bad_level(report) is False

    report: day2.Report = [9, 7, 6, 2, 1]
    # not safe becasue between 6, 2 there is a diff of 4
    assert day2.is_report_unsafe_by_single_bad_level(report) is False

    report: day2.Report = [1, 3, 2, 4, 5]
    # not safe becasue between the sequence is not strictly increasing or strictly decreasing
    # removing element 3 makes it safe
    assert day2.is_report_unsafe_by_single_bad_level(report) is True

    report: day2.Report = [8, 6, 4, 4, 1]
    # not safe becasue between the sequence is not strictly increasing or strictly decreasing
    # 4, 4 is constant
    # removing one of the 4 elements makes it safe
    assert day2.is_report_unsafe_by_single_bad_level(report) is True

    report: day2.Report = [1, 3, 6, 7, 9]
    # this report is safe
    assert day2.is_report_unsafe_by_single_bad_level(report) is False


def test_get_reports_tolerable_by_single_bad_level():
    reports: day2.Reports = day2.read_reports_from_file(day_2_file)
    assert day2.get_reports_tolerable_by_single_bad_level(reports) == 2 + 2
