import logging
import requests
from Config.Server.Server import get_server_url
from Config.Auth.Token.Token_Headers import get_headers
from XrayApi.Common.Response import JiraResponse

server_url = get_server_url()

def get_request(url: str) -> JiraResponse:
    response = requests.get(url, headers=get_headers())
    # TODO refactor error msg
    if response.status_code != 200:
        logging.getLogger().error(f"Error {response.status_code} in response:\n {response.text}")
    return JiraResponse(response)


def post_request(url: str, fields: dict) -> JiraResponse:
    response = requests.post(url, data=fields, headers=get_headers())
    # TODO refactor error msg
    if response.status_code != 200:
        logging.getLogger().error(f"Error {response.status_code} in response:\n {response.text}")
    return JiraResponse(response)


def get_issue_steps(issue_type: str, issue_id: str, field: str) -> JiraResponse:
    url = server_url + f"/rest/raven/2.0/api/{issue_type}/{issue_id}/{field}"

    logging.getLogger().info(f"Requesting {url}")
    return get_request(url)


def create_issue(fields: dict) -> JiraResponse:
    url = server_url + "/rest/api/2/issue"
    logging.getLogger().info("Creating issue...")
    return post_request(url, fields)
