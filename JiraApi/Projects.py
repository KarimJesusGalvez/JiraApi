import logging
import requests
from jira import JIRA
from Config.Auth.Token.Token_Headers import get_headers
from Config.Server.Server import get_server_url

log = logging.getLogger("Jira.Projects")


def get_project_data(jira: JIRA, project_id: str) -> dict[str, str]:
    """project_id: project id, name or key"""
    for project in jira.projects():
        ids = {"name": project.raw["name"], "key": project.raw["key"], "id": project.raw["id"]}
        if project_id in ids.values():
            log.debug(f"Found project {ids}")
            return ids
    msg = f"Project {project_id} not found in list {jira.projects()}"
    log.error(msg)
    raise ValueError(msg)


def get_project_issue_types(jira_server: JIRA, project_id: str) -> dict[str, str]:
    issue_types = {}
    for issue_type in jira_server.project(project_id).raw["issueTypes"]:
        issue_types[issue_type["name"]] = issue_type["description"]
    log.debug(f"Retrieved issue types for project {project_id}, {issue_types}")
    return issue_types

def _parse_meta_issue_fields_type(response):
    raise NotImplementedError("")


def get_fields_for_all_issue_types(jira_server: JIRA, project_id: str) -> dict:
    url = get_server_url() + f"/rest/api/2/issue/createmeta/{project_id}/issuetypes"
    result = {}
    for issue_type in jira_server.project(project_id).raw["issueTypes"]:
        print(f"Searching for {issue_type['name']}({issue_type['id']}) in project {project_id}")
        response = requests.get(url + f"/{issue_type['id']}", headers=get_headers())
        assert response.status_code == 200, f"{response.status_code} Error" \
                                            f"\n URL:{response.request.url}" \
                                            f"\n Headers:{response.raw.headers}" \
                                            f"\n Body:{response.raw._body}"
        result[issue_type['name']] = _parse_meta_issue_fields_type(response.json())
    print(result)
    return result


if __name__ == "__main__":
    from Config import Logs
