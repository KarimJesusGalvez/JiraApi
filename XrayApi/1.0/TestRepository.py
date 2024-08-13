from Config.Logs import create_logger_from_subfolder
from XrayApi.Common.AbstractRequest import server_url, get_request, put_request, post_request, delete_request
from XrayApi.Common.Response import JiraResponse


log = create_logger_from_subfolder(globals()['__file__'], "XrayApi")


def get_project_repositories(project_key: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders"
    return get_request(url)


def get_all_tests_from_repository(project_key: str, folder_id: str) -> JiraResponse:
    return get_tests_from_repository_query(project_key, folder_id)


def get_tests_from_repository_query(project_key: str, folder_id: str, query: str = "") -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders/{folder_id}/tests"
    return get_request(url + query)


def link_repository_to_tests(testplan_id: str, add_tests_ids: list, remove_tests_ids: list) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testplan/{testplan_id}/test"
    data = {"add": add_tests_ids, "remove": remove_tests_ids}
    return put_request(url, data)


def add_tests_to_repository(testplan_id: str, tests_ids: list) -> JiraResponse:
    return link_repository_to_tests(testplan_id, tests_ids, [])


def remove_tests_from_repository(testplan_id: str, tests_ids: list) -> JiraResponse:
    return link_repository_to_tests(testplan_id, [], tests_ids)


def get_folder(project_key: str, folder_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders/{folder_id}"
    return get_request(url)


def create_folder(project_key: str, name: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders/-1"
    return post_request(url, {"name": name})


def update_folder_name(project_key: str, folder_id: str, name: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders/{folder_id}"
    return put_request(url, {"name": name})


def delete_folder_name(project_key: str, folder_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrepository/{project_key}/folders/{folder_id}"
    return delete_request(url)
