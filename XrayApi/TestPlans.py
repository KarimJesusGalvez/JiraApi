import logging
from os import sep

from XrayApi.Common.AbstractRequest import server_url, post_request, get_request
from XrayApi.Common.Response import JiraResponse

log = logging.getLogger(f"Xray.{globals()['__file__'].split(sep)[-1].replace('.py', '')}")

def get_test_plan(testplan_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testplan/{testplan_id}/test"
    return get_request(url)


def link_test_plan_to_tests(testplan_id: str, add_tests_ids: list, remove_tests_ids: list) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testplan/{testplan_id}/test"
    data = {"add": add_tests_ids, "remove": remove_tests_ids}
    return post_request(url, data)


def add_tests_to_test_plan(testplan_id: str, tests_ids: list) -> JiraResponse:
    return link_test_plan_to_tests(testplan_id, tests_ids, [])


def remove_tests_from_test_plan(testplan_id: str, tests_ids: list) -> JiraResponse:
    return link_test_plan_to_tests(testplan_id, [], tests_ids)


def get_plan_executions(testplan_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testplan/{testplan_id}/testexecution"
    return get_request(url)


def add_plan_executions(testplan_id: str, add_execution_ids: list, remove_execution_ids: list, add_tests: bool = True,) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testplan/{testplan_id}/test"
    data = {"addTestsToPlan": "true" if add_tests else "false",
            "add": add_execution_ids, "remove": remove_execution_ids}
    return post_request(url, data)


if __name__ == "__main__":
    from Config import Logs
