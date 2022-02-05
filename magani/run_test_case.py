import dash_bootstrap_components as dbc
from dash import html

from magani.utils.file_util import read_project_file, write_project_file
from magani.http.http_client import HttpClient


class RunTestCase:

    def __init__(self):
        self.html_response = ""

    def run(self, test_case):
        response = HttpClient(test_case["API"]).method(test_case["Method"])(test_case["Body"])
        self.html_response = html.Div(
            [
                html.H1("Test Case : {}".format(test_case["API"]), style={"text-align": "center", "color": "red"}),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2("Method : {}".format(test_case["Method"]),
                                    style={"text-align": "left", "color": "yellow"}),
                            style={"width": 6}
                        ),
                        dbc.Col(
                            html.H2("Status : {}".format(response.status_code),
                                    style={"text-align": "right", "color": "green"}),
                            style={"width": 6}
                        ),
                    ],
                ),
                html.P("Response : {}".format(response.body))
            ]
        )
        test_case["ResponseBody"] = response.body
        test_case["StatusCode"] = response.status_code
        test_case["Status"] = response.status
        return self.html_response

    def get_html(self):
        return self.html_response


def layout(pathname):
    lt = str(pathname).strip("/").split("/")
    project = lt[0]
    action = lt[-1]
    if not (action == "test"):
        return

    api_id = lt[1] if len(lt) == 3 else None

    projects_new = read_project_file()

    lt = []
    for p in projects_new:
        if p["Project"] == project:
            if api_id:
                for tc in p["TestCase"]:
                    if tc["ID"] == api_id:
                        lt.append(RunTestCase().run(tc))
            else:
                lt = [
                    html.H1("Testing project {} ".format(project), style={"text-align": "center", "color": "Blue"})
                ]
                for test_case in p["TestCase"]:
                    lt.append(RunTestCase().run(test_case))

    write_project_file(projects_new)
    return dbc.Container(
        lt
    )
