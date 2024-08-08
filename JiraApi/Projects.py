import logging
from typing import Any
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


def _parse_meta_issue_fields_name(response: dict):
    result = {}
    for data in response["values"]:
        if data["name"] == "Issue Type":
            continue
        result[data["name"]] = data
    return result


def _print_meta_issue_dict(field: dict, depth: int) -> str:
    sep = "    " * depth
    msg = "\n"
    for key, value in field.items():
        if isinstance(value, dict):
            msg += _print_meta_issue_dict(value, depth + 1)
        else:
            msg += f"{sep}{key}, {value}"
    return msg


def _parse_meta_issue_fields_data_type(field: dict) -> str:
    return field["schema"]["type"]


def _print_meta_issue_fields_data(field: dict) -> str:
    msg = ""
    sep = "    "

    for key, value in field.items():
        if isinstance(value, dict):
            _print_meta_issue_dict(value, 1)
        elif isinstance(value, list):
            for val in value:
                msg = f"{sep}[{key}"
                if isinstance(value, dict):
                    msg += _print_meta_issue_dict(value, 2)
                else:
                    msg += f"\n{sep * 2}{val}"
                msg += f"\n{sep}]"
        else:
            msg += f"{sep}{key}, {value}"
    return msg


def _parse_meta_issue_fields_type(response: dict) -> dict:
    result = {}
    for field, data in _parse_meta_issue_fields_name(response).items():
        log.debug(f"Parsing field {field}")
        log.debug(_print_meta_issue_fields_data(data))
        result[field] = _parse_meta_issue_fields_data_type(data)
    return result


def get_fields_for_all_issue_types(jira_server: JIRA, project_id: str) -> dict[str, tuple[dict, dict]]:
    result = {}
    for issue_type in jira_server.project(project_id).raw["issueTypes"]:
        log.info(f"Searching for {issue_type['name']}({issue_type['id']}) in project {project_id}")
        response = get_meta_issue_fields(project_id, issue_type['id'])
        template = create_dict_template_for_issue(issue_type['name'], response, project_id)
        fields = _parse_meta_issue_fields_type(response)
        log.info(f"Issue type {issue_type['name']} has fields {fields}")
        result[issue_type['name']] = (fields, template)
    return result


def get_meta_issue_fields(project_id: str, issue_id: str) -> dict:
    url = get_server_url() + f"/rest/api/2/issue/createmeta/{project_id}/issuetypes"
    response = requests.get(url + f"/{issue_id}", headers=get_headers())
    assert response.status_code == 200, f"{response.status_code} Error" \
                                        f"\n URL:{response.request.url}" \
                                        f"\n Headers:{response.raw.headers}" \
                                        f"\n Body:{response.raw._body}"
    return response.json()


def _generate_empty_dataset_for_field(data_type: str, project_id: str) -> Any:
    if data_type == "array":
        return []
    elif data_type == "string":
        return ""
    elif data_type == "project":
        return {"id": project_id}
    elif data_type == "user":
        # TODO return jira.user data
        return {}


def create_dict_template_for_issue(issue_name: str, response: dict, project_id: str) -> dict:
    field_dict = {'issuetype': {'name': f'{issue_name}'}}
    for field, data in _parse_meta_issue_fields_name(response).items():
        if _parse_meta_issue_fields_data_required(data):
            field_dict[field] = _get_dict_template_for_field(data, field, project_id)
    return field_dict


def _get_dict_template_for_field(data: dict, field: str, project_id: str) -> dict:
    data_type = _parse_meta_issue_fields_data_type(data)
    log.debug(f"Found '{'mandatory' if _parse_meta_issue_fields_data_required(data) else 'optional'}' "
              f"field '{field}', with type '{data_type}'")
    return _generate_empty_dataset_for_field(data_type, project_id)


def _parse_meta_issue_fields_data_required(field: dict) -> str:
    return field["required"]


if __name__ == "__main__":
    from Config import Logs
