import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import json
from magani_server import app
from magani.utils.card_util import CreateTestCard
from magani.utils.modal_util import CreateTestCaseModal
from datetime import datetime
from magani.utils.file_util import read_project_file, write_project_file


def get_test_cards(project):
    projects = read_project_file()
    test_cases = [y["TestCase"] for y in projects if y["Project"] == project]
    test_cases = test_cases[0] if test_cases else test_cases

    test_case_cards = [
        CreateTestCard(project, y["API"], y["ID"], y["Method"], y["Status"]).get() for y in test_cases
    ]

    test_create_button = dbc.Button("+", id="Create_Test_Case_Btn_ID", style={"width": "20rem", "height": "8rem"})

    test_case_cards.append(test_create_button)

    i = 3
    cards = [
        dbc.Row(
            [
                dbc.Col(
                    y,
                    width="auto"
                )
                for y in test_case_cards[x * i: x * i + i if x * i + i < len(test_case_cards) else len(test_case_cards)]
            ]

        )

        for x in range(i)
    ]
    return cards


def layout(project):
    project = project.replace("%20"," ")
    projects = read_project_file()
    print("[x[Project] for x in projects] :", [x["Project"] for x in projects])
    is_exist = project in [x["Project"] for x in projects]
    if is_exist:
        return html.Div(
            [
                html.H1("Project : {}".format(project), style={"text-align": "center"}),
                dbc.Container(
                    get_test_cards(project),
                    className="my-1"
                ),
                CreateTestCaseModal(project).get()
            ],
        )
    else:
        return dbc.Container(
            [
                html.H1("Invalid Project : {}".format(project))
            ]
        )


@app.callback(Output('Create_Test_Case_Submit_ID', 'disabled'),
              [Input("Test_Case_API_ID", "value"), Input("Test_Case_Method_ID", "value")])
def create_test_submit_btn_update(email, message):
    if email and message:
        return False
    return True


@app.callback(
    Output("Create_Test_Case_Modal_ID", "is_open"),
    [Input("Create_Test_Case_Btn_ID", "n_clicks"), Input('Create_Test_Case_Submit_ID', 'n_clicks')],
    [State("Create_Test_Case_Modal_ID", "is_open"),
     State("Test_Case_Project_ID", "value"),
     State("Test_Case_API_ID", "value"),
     State("Test_Case_Method_ID", "value"),
     State("Test_Case_Body_ID", "value")],
)
def toggle_modal(n1, n2, is_open, project, api, method, body):
    print(n1, n2)
    if n1 or n2:
        if api and method:
            print(api, method)
            projects = read_project_file()
            p = [x for x in projects if x["Project"] == project][0]
            api_id = str(datetime.now()).replace(" ", "").replace(":", "").replace("-", "").replace(".", "")

            t = {
                "ID": "{}_{}".format(project, api_id),
                "API": api,
                "Body": json.dumps(body) if body else None,
                "Method": method,
                "Status": "Success"
            }
            p["TestCase"].append(t)
            write_project_file(projects)
        return not is_open
    return is_open
