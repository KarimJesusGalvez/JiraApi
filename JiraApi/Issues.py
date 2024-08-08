from jira import JIRA, Issue
from Config.Logs import create_logger_from_subfolder

log = create_logger_from_subfolder(globals()['__file__'])


def search_issues(jira_server: JIRA, query: str) -> list[Issue]:
    query = escape_reserved_words_in_query(query)
    log.info(f"Executing query: {query} ...\n")
    existing_issues = jira_server.search_issues(query, maxResults=2000)

    issues_found = ""
    for issue in existing_issues:
        issues_found += f'\n{issue} {jira_server.issue(issue).fields.summary}'
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


def check_existing_issue(jira_server: JIRA, project_id: int, issue_type: str, summary: str) -> list | None:
    issues = search_issues(jira_server, f'project = {project_id} '
                                        f'AND type = "{issue_type}" '
                                        f'AND summary ~ "\\"{summary}\\""')
    if len(issues) > 0:
        log.warning(f"{len(issues)} Issue/s found for {summary}, {issues[0].key}")
    else:
        log.info("Similar issue not found")
    return issues


def update_link(jira_server: JIRA, link_type: str, in_query: str, out_query: str) -> None:
    if not check_link_name(jira_server, link_type):
        raise ValueError(f"Invalid link {link_type}")

    in_issues = search_issues(jira_server, in_query)
    out_issues = search_issues(jira_server, out_query)
    for in_issue in in_issues:  # if issues > 1 version is equal
        for out_issue in out_issues:  # if issues > 1 version is equal
            log.info(f"Updating link; {str(in_issue.fields.issuetype)} "
                     f"{in_issue.key} -> "
                     f"{link_type} -> "
                     f"{str(out_issue.fields.issuetype)} {out_issue.key} ...")
            jira_server.create_issue_link(link_type, in_issue.key, out_issue.key)


def check_link_name(jira_server: JIRA, link_type: str) -> bool:
    valid_names = jira_server.issue_link_types()
    if link_type in valid_names:
        log.debug(f"Link {link_type} is valid")
        return True
    else:
        log.warning(f"Found invalid link name '{link_type}', valid names are {[data.name for data in valid_names]}")
        return False


def create_issue_if_not_existing(jira_server: JIRA, project_id: int, issue_dict: dict) -> Issue | None:
    if not check_existing_issue(jira_server, project_id, "Test", issue_dict["Summary"]):
        return create_issue(jira_server, issue_dict)
    else:
        log.warning("Issue/s found, Skipping Issue creation")


def create_issue(jira_server: JIRA, issue_dict: dict) -> Issue | None:

    new_issue = jira_server.create_issue(fields=issue_dict)
    log.warning(f"Created new {new_issue.fields.issuetype} issue: {new_issue.key}")
    return new_issue
