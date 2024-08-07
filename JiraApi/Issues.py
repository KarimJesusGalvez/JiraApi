import logging
from jira import JIRA, Issue


log = logging.getLogger("Jira.Issues")


def execute_query(jira: JIRA, query: str) -> list[Issue]:
    query = escape_reserved_words_in_query(query)
    log.info(f"Executing query: {query} ...\n")
    existing_issues = jira.search_issues(query, maxResults=2000)

    issues_found = ""
    for issue in existing_issues:
        issues_found += f'\n{issue} {jira.issue(issue).fields.summary}'
    if issues_found:
        log.info(f"Found {int(len(existing_issues))} issue/s:" + issues_found)
    else:
        log.warning("No issue/s found in query...")
    return existing_issues


def escape_reserved_words_in_query(query: str) -> str:
    query = query.replace("[", "\\\\[").replace("]", "\\\\]")
    query = query.replace(".", "\\\\.").replace(",", "\\\\,")
    query = query.replace("+", "\\\\+").replace("|", "\\\\|")
    query = query.replace("?", "\\\\?").replace("*", "\\\\*")
    query = query.replace("%", "\\\\%").replace("^", "\\\\^")
    query = query.replace("$", "\\\\$").replace("#", "\\\\#")
    query = query.replace("@", "\\\\@").replace(";", "\\\\;")
    return query


def check_existing_issue(jira: JIRA, project_id: int, issue_type: str, summary: str) -> list | None:
    issues = execute_query(jira, f'project = {project_id} AND type = "{issue_type}" AND summary ~ "\\"{summary}\\""')
    if len(issues) > 0:
        log.warning(f"{len(issues)} Issue/s found for {summary}, {issues[0].key}")
    else:
        log.info("Similar issue not found")
    return issues


if __name__ == "__main__":
    from Config import Logs
