from XrayApi.Common.AbstractRequest import server_url, get_request, put_request
from XrayApi.Common.Response import JiraResponse


def get_run_tests(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}"
    return get_request(url)


def get_test_run(run_id: str, test_id: str) -> JiraResponse:
    url = server_url + "/rest/raven/1.0/api/testrun"
    query = f"?testExecIssueKey={run_id}&testIssueKey={test_id}"
    return get_request(url + query)


def get_defined_run_status() -> JiraResponse:
    url = server_url + "/rest/raven/1.0/api/settings/teststatuses"
    return get_request(url)


def update_run_by_id(run_id: str, status: str, comment: str, assignee: str,
                     defects: dict, evidences: dict,
                     examples: list[dict], steps: list[dict]) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}"
    data = {"status": status, "comment": comment,
            "assignee": assignee, "defects": defects, "evidences": evidences,
            "examples": examples, "steps": steps,
            }
    put_request(url, data)


def get_run_status(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/status"
    return get_request(url)


def update_run_status(run_id: str, status_name: str="") -> JiraResponse:
    if not status_name:
        names = [entry["name"] for entry in get_defined_run_status().parsed]
        status_name = input(f"Type an status name from list: {names}\n")
    update_run_by_id(run_id, status_name, "", "", {}, {}, [], [])


if __name__ == "__main__":
    from Config import Logs
