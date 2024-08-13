from jira import JIRA
from jira.resources import Field
from Config.Logs import create_logger_from_subfolder
from typing import Any

from JiraApi.Projects import get_project_data

log = create_logger_from_subfolder(globals()['__file__'])


def get_fields_for_meta_issue(jira_server: JIRA, project_id: str, issue_id: str) -> list[Field]:
    return jira_server.project_issue_fields(project_id, issue_id)


def create_dict_template_for_issue(issue_id: str, project_id: str, fields: list[Field]) -> dict:
    field_dict = {'issuetype': {'id': f'{issue_id}'}}
    for field in fields:
        field_dict[field] = _get_dict_template_for_field(field, project_id)
    return field_dict


def get_fields_for_all_issue_types(jira_server: JIRA, project_id: str) -> dict[str, tuple[list[Field], dict]]:
    result = {}
    for issue_type in get_all_issue_types_data(jira_server, project_id):
        log.info(f"Searching for {issue_type['name']}({issue_type['id']}) in project {project_id}")
        response = get_fields_for_meta_issue(jira_server, project_id, issue_type['id'])
        log.info(f"Issue type {issue_type['name']} has fields {response}")
        template = create_dict_template_for_issue(issue_type['id'], project_id, response)
        result[issue_type['name']] = (response, template)
    return result


def get_all_issue_types_data(jira_server: JIRA, project_id: str) -> dict:
    return jira_server.project(project_id).raw["issueTypes"]


def _parse_meta_issue_fields_name(response: dict) -> dict:
    result = {}
    for data in response["values"]:
        if data["name"] == "Issue Type":
            continue
        result[data["name"]] = data
    return result


def _print_meta_issue_dict(field: dict, depth: int) -> str:
    whitespace = "    " * depth
    msg = "\n"
    for key, value in field.items():
        if isinstance(value, dict):
            msg += _print_meta_issue_dict(value, depth + 1)
        else:
            msg += f"{whitespace}{key}, {value}"
    return msg


def _parse_meta_issue_fields_data_type(field: dict) -> str:
    return field["schema"]["type"]


def _print_meta_issue_fields_data(field: dict) -> str:
    msg = ""
    whitespace = "    "

    for key, value in field.items():
        if isinstance(value, dict):
            _print_meta_issue_dict(value, 1)
        elif isinstance(value, list):
            for val in value:
                msg = f"{whitespace}[{key}"
                if isinstance(value, dict):
                    msg += _print_meta_issue_dict(value, 2)
                else:
                    msg += f"\n{whitespace * 2}{val}"
                msg += f"\n{whitespace}]"
        else:
            msg += f"{whitespace}{key}, {value}"
    return msg


def _parse_meta_issue_fields_type(response: dict) -> dict:
    result = {}
    for field, data in _parse_meta_issue_fields_name(response).items():
        log.debug(f"Parsing field {field}")
        log.debug(_print_meta_issue_fields_data(data))
        result[field] = _parse_meta_issue_fields_data_type(data)
    return result


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


def _get_dict_template_for_field(field: Field, project_id: str) -> dict:
    log.debug(f"Found '{'mandatory' if field.raw['required'] else 'optional'}' "
              f"field '{field}', with type '{field.raw['schema']['type']}'")
    return _generate_empty_dataset_for_field(field.raw['schema']['type'], project_id)


def _parse_meta_issue_fields_data_required(field: dict) -> str:
    return field["required"]
