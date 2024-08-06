from XrayApi.Common.AbstractRequest import server_url, get_request, put_request, post_request, delete_request
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
    return put_request(url, data)


def get_run_status(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/status"
    return get_request(url)


def update_run_status(run_id: str, status_name: str = "") -> JiraResponse:
    if not status_name:
        names = [entry["name"] for entry in get_defined_run_status().parsed]
        status_name = input(f"Type an status name from list: {names}\n")
    return update_run_by_id(run_id, status_name, "", "", {}, {}, [], [])


def get_run_defects(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/defect"
    return get_request(url)


def link_run_defects(run_id: str, defects_ids: list[str]) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/defect"
    return post_request(url, defects_ids)


def remove_run_defects(run_id: str, defect_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/defect/{defect_id}"
    return delete_request(url)


def get_run_evidence(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/attachment"
    return get_request(url)


def add_evidence_to_run(run_id: str, file_data: bytes, file_name: str, content_type: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/attachment"
    data = {"data": file_data, "filename": file_name, "contentType": content_type}
    return post_request(url, data)


def remove_run_evidences(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/attachment"
    return delete_request(url)


def remove_run_evidence_by_id(run_id: str, attachment_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/attachment/{attachment_id}"
    return delete_request(url)


def get_run_comment(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/comment"
    return get_request(url)


def update_run_comment(run_id: str, comment: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/comment"
    return put_request(url, comment)


def get_run_example(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/example"
    return get_request(url)


def get_run_steps(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/step"
    return get_request(url)


def get_run_asignee(run_id: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/asignee"
    return get_request(url)


def update_run_asignee(run_id: str, user_name: str) -> JiraResponse:
    url = server_url + f"/rest/raven/1.0/api/testrun/{run_id}/assignee"
    query = f"?user={user_name}"
    return put_request(url + query, "")


if __name__ == "__main__":
    from Config import Logs
