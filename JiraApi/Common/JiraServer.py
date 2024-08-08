import traceback
from typing import Any
from jira import JIRA
from Config.Auth.Token.Token_Headers import read_token
from Config.Server.Server import get_server_url


class JiraServer:
    """Context manager for JIRA instances"""

    def __init__(self) -> None:
        self.server = None

    def __enter__(self) -> JIRA:
        headers = JIRA.DEFAULT_OPTIONS["headers"]
        headers["Authorization"] = f"Bearer {read_token()}"
        log.info("Starting Jira server...")
        self.server = JIRA(server=get_server_url(), options={"headers": headers, 'verify': True}, get_server_info=True)
        return self.server

    def __exit__(self, exc_type: Exception, exc_val: Any, exc_tb: traceback) -> None:
        if self.server:
            self.server.close()
        log.info("Jira server closed//")
