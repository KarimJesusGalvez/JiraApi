import requests

from Config.Auth.Token.Token_Headers import get_headers
from XrayApi.Common.AbstractRequest import server_url, get_request
from XrayApi.Common.Response import JiraResponse


def export_feature(query: str) -> JiraResponse:
    url = server_url + "/rest/raven/1.0/export/test"
    url += (query if query.startswith("?") else "?" + query)
    headers = get_headers()
    headers["Accept"] = "application/octet-stream"
    return JiraResponse(requests.get(url=url, headers=headers))


def export_features_by_filter(filter_id: str, compress: bool = False) -> JiraResponse:
    return export_feature(f"filter={filter_id}" + ("&fz=true" if compress else ""))


def export_features_by_test_id(test_ids: list[str], compress: bool = False) -> JiraResponse:
    query = "keys="
    for test in test_ids:
        query += test + ";"
    if compress:
        query += "&fz=true"
    return export_feature(query)


if __name__ == "__main__":
    from Config import Logs
