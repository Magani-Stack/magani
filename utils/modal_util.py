import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

methods = ["GET", "POST"]


class CreateModal:

    def __init__(self):
        self.modal = None

    def get(self):
        return self.modal


class CreateTestCaseModal(CreateModal):

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.modal = dbc.Modal(
            [
                dbc.ModalHeader("Test Case"),
                dbc.ModalBody([
                    self.get_form()
                ]),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Create", id="Create_Test_Case_Submit_ID", className="ml-auto", n_clicks=0, disabled=True
                        )
                    ]
                ),
            ],
            id="Create_Test_Case_Modal_ID",
            centered=True,
        )

    def get_form(self):
        project_input = dbc.FormGroup(
            [
                dbc.Label("API", html_for="Test_Case_Project_ID"),
                dcc.Dropdown(id="Test_Case_Project_ID", options=[{'label': self.project, 'value': self.project}],
                             value=self.project,
                             multi=False),
            ]
        )

        api_input = dbc.FormGroup(
            [
                dbc.Label("API", html_for="Test_Case_API_ID"),
                dbc.Input(type="text", id="Test_Case_API_ID", placeholder="Enter the API"),
            ]
        )

        method_input = dbc.FormGroup(
            [
                dbc.Label("Method", html_for="Test_Case_API_ID"),
                dcc.Dropdown(id="Test_Case_Method_ID", options=[{'label': x, 'value': x} for x in methods],
                             multi=False),
            ]
        )

        form = dbc.Form([project_input, api_input, method_input])
        return form
