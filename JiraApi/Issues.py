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


def update_link(jira: JIRA, link_type: str, in_query: str, out_query: str) -> None:
    if not check_link_name(jira, link_type):
        raise ValueError(f"Invalid link {link_type}")

    in_issues = execute_query(jira, in_query)
    out_issues = execute_query(jira, out_query)
    for in_issue in in_issues:  # if issues > 1 version is equal
        for out_issue in out_issues:  # if issues > 1 version is equal
            log.info(f"Updating link; {str(in_issue.fields.issuetype)} "
                        f"{in_issue.key} -> "
                        f"{link_type} -> "
                        f"{str(out_issue.fields.issuetype)} {out_issue.key} ...")
            jira.create_issue_link(link_type, in_issue.key, out_issue.key)


def check_link_name(jira: JIRA, link_type: str) -> bool:
    valid_names = jira.issue_link_types()
    if link_type in valid_names:
        log.debug(f"Link {link_type} is valid")
        return True
    else:
        log.warning(f"Found invalid link name '{link_type}', valid names are {[data.name for data in valid_names]}")
        return False

if __name__ == "__main__":
    from Config import Logs
