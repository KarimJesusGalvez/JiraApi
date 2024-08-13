from Config.Logs import create_logger_from_subfolder
from XrayApi.Common.AbstractRequest import get_issue_steps, get_request, server_url
from XrayApi.Common.Response import JiraResponse


log = create_logger_from_subfolder(globals()['__file__'], "XrayApi")


def get_test_plan_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "testplans")


def get_test_executions_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "testexecutions")


def get_test_preconditions_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "preconditions")


def get_test_sets_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "testsets")


def get_test_plans_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "testplans")


def get_test_runs_from_test(issue_id: str) -> JiraResponse:
    return get_test_field(issue_id, "testruns")


def create_test(fields: dict):
    # TODO
    raise NotImplementedError("")
    fields["issuetype"] = {"name": "Test"}
    create_issue(fields=fields)


def export_test_data_to_json_from_keys(keys: list) -> JiraResponse:
    query = "keys="
    for key in keys:
        query += key + ";"
    return export_test_data_to_json(query[:-1])


def export_test_data_to_json_from_filter(filter_id: str) -> JiraResponse:
    query = f"filter={filter_id}"
    return export_test_data_to_json(query)


def export_test_data_to_json_from_jql(jql: str) -> JiraResponse:
    query = f"jql={jql}"
    return export_test_data_to_json(query)


def export_test_data_to_json(query: str) -> JiraResponse:
    url = server_url + "/rest/raven/2.0/api/test"
    url = url + "?" + query
    return get_request(url)


def get_test_field(issue_id: str, field: str) -> JiraResponse:
    return get_issue_steps("test", issue_id, field)
