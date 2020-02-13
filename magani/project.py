import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
from server import app
from utils.card_util import CreateTestCard
from utils.modal_util import CreateTestCaseModal
from datetime import datetime


def get_test_cards(project):
    projects = eval(open("data/projects/projects.json", "r").read(), {"null": None})
    test_cases = [y["TestCase"] for y in projects if y["Project"] == project]
    test_cases = test_cases[0] if test_cases else test_cases

    test_case_cards = [
        CreateTestCard(project, y["API"], y["ID"], y["Method"]).get() for y in test_cases
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
    projects = eval(open("data/projects/projects.json", "r").read(), {"null": None})
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
     State("Test_Case_Method_ID", "value")],
)
def toggle_modal(n1, n2, is_open, project, api, method):
    print(n1, n2)
    if n1 or n2:
        if api and method:
            print(api, method)
            projects = eval(open("data/projects/projects.json", "r").read(), {"null": None})
            p = [x for x in projects if x["Project"] == project][0]
            api_id = str(datetime.now()).replace(" ", "").replace(":", "").replace("-", "").replace(".", "")

            t = {
                "ID": "{}_{}".format(project, api_id),
                "API": api,
                "Body": None,
                "Method": method,
                "Status": "Success"
            }
            p["TestCase"].append(t)
            with open("data/projects/projects.json", "w") as f:
                f.writelines(json.dumps(projects, indent=4, sort_keys=True))
                f.write("\n")
        return not is_open
    return is_open
