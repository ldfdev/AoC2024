Report = list[int]
Reports = list[Report]


def read_reports_from_file(file_path: str) -> Reports:
    with open(file_path) as reader:
        lines: list[str] = reader.readlines()
    reports: Reports = [[int(x) for x in line.strip().split()] for line in lines]
    return reports


def all_numbers_have_same_sign(numbers: list[int]) -> bool:
    return all(number > 0 for number in numbers) or all(
        number < 0 for number in numbers
    )


def is_report_safe(report: Report) -> bool:
    diffs: list[int] = [current_ - next_ for current_, next_ in zip(report, report[1:])]
    if 0 in diffs:
        return False
    # check if we have all negative or all positive numbers
    if not all_numbers_have_same_sign(diffs):
        return False

    # check if all diffs are 1, 2 or 3
    diffs = set(abs(diff) for diff in diffs)
    expected_diffs = [1, 2, 3]
    for diff in expected_diffs:
        if diff not in diffs:
            continue
        diffs.remove(diff)
    return len(diffs) == 0


def get_safe_reports(reports: Reports) -> int:
    return len([Report for report in reports if is_report_safe(report)])


def is_report_unsafe_by_single_bad_level(report: Report) -> bool:
    if is_report_safe(report):
        return False
    for i in range(len(report)):
        new_report = report[:i] + report[i + 1 :]
        if is_report_safe(new_report):
            return True
    return False


def get_reports_tolerable_by_single_bad_level(reports: Reports) -> int:
    return get_safe_reports(reports) + len(
        [Report for report in reports if is_report_unsafe_by_single_bad_level(report)]
    )
