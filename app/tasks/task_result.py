from typing import Literal, TypedDict


class TaskResult(TypedDict):
    status: Literal["SUCCESS", "WARNING", "FAILURE", "SKIPPED"]
    message: str | None


def success_result(message: str = None) -> TaskResult:
    result: TaskResult = {"status": "SUCCESS", "message": message}
    return result


def warning_result(message: str) -> TaskResult:
    result: TaskResult = {"status": "WARNING", "message": message}
    return result


def failure_result(message: str) -> TaskResult:
    result: TaskResult = {"status": "FAILURE", "message": message}
    return result


def skipped_result(message: str) -> TaskResult:
    result: TaskResult = {"status": "SKIPPED", "message": message}
    return result
