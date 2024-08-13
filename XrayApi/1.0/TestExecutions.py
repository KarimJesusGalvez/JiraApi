import logging
from os import sep

from XrayApi.Common.AbstractRequest import server_url, get_request, post_request, delete_request
from XrayApi.Common.Response import JiraResponse

log = logging.getLogger(f"Xray.{globals()['__file__'].split(sep)[-1].replace('.py', '')}")


def get_tests_in_execution(execution_id: str, details: bool = False) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testexec/{execution_id}/test"
    query = f"?detailed={'true' if details else 'false'}"
    return get_request(url + query)


def link_test_to_execution(execution_id: str, add_tests_ids: list, remove_tests_ids: list) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testexec/{execution_id}/test"
    data = {"add": add_tests_ids, "remove": remove_tests_ids}
    return post_request(url, data)


def add_tests_to_execution(execution_id: str, tests_ids: list) -> JiraResponse:
    return link_test_to_execution(execution_id, tests_ids, [])


def remove_tests_from_execution(execution_id: str, tests_ids: list) -> JiraResponse:
    return link_test_to_execution(execution_id, [], tests_ids)


def create_test_execution(execution_id: str, details: bool = False) -> JiraResponse:
    # TODO wait for jira createissue implementation
    raise NotImplementedError("Wait for jira createissue implementation")


def delete_test_execution(execution_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testexec/{execution_id}/test"
    return delete_request(url)


def export_execution_results_from_test_plan(test_plan_id: str) -> JiraResponse:
    return export_execution_results(f"testPlanKey={test_plan_id}")


def export_execution_results_from_filter(filter_id: str) -> JiraResponse:
    return export_execution_results(f"savedFilterId={filter_id}")


def export_execution_results_from_test(test_id: str) -> JiraResponse:
    return export_execution_results(f"testKey={test_id}")


def export_execution_results_with_fields(query: str, fields: list[str]):
    #TODO add pagination
    query += "&includeTestFields="
    for field in fields:
        query += field + ","
    export_execution_results(query[:-1])


def export_execution_results(query: str) -> JiraResponse:
    url = server_url + "/rest/raven/1.0/testruns"
    return get_request(url + (query if query.startswith("?") else "?" + query))


if __name__ == "__main__":
    from Config import Logs
