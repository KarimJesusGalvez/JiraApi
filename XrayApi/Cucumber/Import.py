import requests
from Config.Auth.Token.Token_Headers import get_headers
from Config.Logs import create_logger_from_subfolder
from XrayApi.Common.AbstractRequest import server_url
from XrayApi.Common.Response import JiraResponse

log = create_logger_from_subfolder(globals()['__file__'], "XrayApi")


def import_feature(feature: bytes, project_short_name: str, update_repository: bool) -> JiraResponse:
    url = server_url + "/rest/raven/1.0/import/feature"
    query = f"?projectKey={project_short_name}&updateRepository={'true' if update_repository else 'false'}"
    headers = get_headers()
    headers["Content-Type"] = "multipart/form-data"
    response = requests.post(url + query, headers=headers, params={"-F": feature})
    return JiraResponse(response)


def get_file_from_path(target_path: str) -> list[str]:
    with open(target_path, "r") as file:
        data = file.readlines()
    if "language:" in data[0] and ":en" not in data[0]:
        msg = f"Cannot import, Feature is not in English in path {target_path}"
        log.error(msg)
        raise ValueError(msg)
    else:
        return data
