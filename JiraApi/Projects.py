import logging
from jira import JIRA

log = logging.getLogger("Jira.Projects")


def get_project_data(jira: JIRA, project_id: str) -> list[str, str, str]:
    """project_id: project id, name or key"""
    ids = []
    for project in jira.projects():
        ids = [project.raw["name"], project.raw["key"], project.raw["id"]]
        if project_id in ids:
            log.debug(f"Found project {ids}")
            return ids
    msg = f"Project {project_id} not found in list {jira.projects()}"
    log.error(msg)
    raise ValueError(msg)


if __name__ == "__main__":
    from Config import Logs