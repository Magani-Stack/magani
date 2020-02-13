import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from utils.file_util import read_project_file, write_project_file
from utils.http_client import HttpClient


def layout(pathname):
    lt = str(pathname).strip("/").split("/")
    project = lt[0]
    action = lt[-1]
    if not (action == "test"):
        return

    api_id = lt[1] if len(lt) == 3 else None

    projects_new = read_project_file()
    project_test = [p for p in projects_new if p["Project"] == project][0]
    if api_id:
        tcs = [tc for tc in project_test["TestCase"] if tc["ID"] == api_id][0]
        response = HttpClient(tcs["API"]).get()
        return dbc.Container(
            [
                html.H1("Test Case : {}".format(tcs["API"])),
                html.H2("Status : {}".format(response.status_code)),
                html.P("Response : {}".format(response.body.decode("utf-8")))
            ]
        )
    else:
        lt = [
            html.H1("Testing project {} ".format(project))
        ]
        for test_case in project_test["TestCase"]:
            response = HttpClient(test_case["API"]).get()
            lt.append(html.Div(
                [
                    html.H1("Test Case : {}".format(test_case["API"])),
                    html.H2("Status : {}".format(response.status_code)),
                    html.P("Response : {}".format(response.body))
                ]
            ))

        return dbc.Container(
            lt
        )
