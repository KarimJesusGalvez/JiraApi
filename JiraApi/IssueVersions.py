import logging
from jira import JIRA
from JiraApi.Issues import search_issues
from JiraApi.JiraServer import JiraServer

log = logging.getLogger("Jira.Issues.Version")


def update_fix_versions(jira_server: JIRA, issue_id: str, fix_version: str) -> None:
    log.info(f"Updating steps in issue {issue_id}")
    jira_server.issue(issue_id).update({'fixVersions': [{'name': fix_version}]})


def update_fix_version_in_issues(fix_version: str, query: str) -> None:
    with JiraServer() as jira:
        for issue in search_issues(jira, query):
            update_fix_versions(jira, issue.key, fix_version)


def input_project_fix_versions_for_project(jira_server: JIRA, project_id: str) -> str:
    fix_versions = get_project_fix_versions(jira_server, project_id)
    while (selected := input(f"Select an issue type from the list:\n{fix_versions}\n")) \
            and selected not in fix_versions:
        log.error(f"'{selected}' is not a Version...")
    return selected


def get_project_fix_versions(jira_server: JIRA, project_id: str) -> list[str]:
    versions = []
    for version in jira_server.project_versions(project_id):
        versions.append(version.raw["name"])
    log.debug(f"Retrieved versions for project {project_id}, {versions}")
    return versions


if __name__ == "__main__":
    from Config import Logs
