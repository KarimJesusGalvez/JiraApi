import logging

from XrayApi.Common.AbstractRequest import server_url, get_request, post_request, delete_request
from XrayApi.Common.Response import JiraResponse

log = logging.getLogger("Xray.Executions")


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


if __name__ == "__main__":
    from Config import Logs
