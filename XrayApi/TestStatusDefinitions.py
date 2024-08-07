from XrayApi.Common.AbstractRequest import get_request, server_url
from XrayApi.Common.Response import JiraResponse


def get_defined_run_status() -> JiraResponse:
    url = server_url + "/rest/raven/1.0/api/settings/teststatuses"
    return get_request(url)


def get_defined_step_status() -> JiraResponse:
    url = server_url + "/rest/raven/1.0/api/settings/teststepstatuses"
    return get_request(url)
