import logging
from jira import JIRA

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




if __name__ == "__main__":
    from Config import Logs
