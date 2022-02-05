import dash_bootstrap_components as dbc
from dash import dcc

methods = ["GET", "POST", "PUT", "DELETE"]


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
        print("self.project : ", self.project)
        project_input = dbc.Form(
            [
                dbc.Label("Project", html_for="Test_Case_Project_ID"),
                dcc.Dropdown(id="Test_Case_Project_ID", options=[{'label': self.project, 'value': self.project}],
                             value=self.project,
                             multi=False),
            ]
        )

        api_input = dbc.Form(
            [
                dbc.Label("API", html_for="Test_Case_API_ID"),
                dbc.Input(type="text", id="Test_Case_API_ID", placeholder="Enter the API"),
            ]
        )

        method_input = dbc.Form(
            [
                dbc.Label("Method", html_for="Test_Case_Method_ID"),
                dcc.Dropdown(id="Test_Case_Method_ID", options=[{'label': x, 'value': x} for x in methods],
                             multi=False),
            ]
        )

        body_input = dbc.Form(
            [
                dbc.Label("Body : JSON", html_for="Test_Case_Body_ID"),
                dcc.Textarea(id="Test_Case_Body_ID", style={"width": "100%"}),
            ]
        )

        form = dbc.Form([project_input, api_input, method_input, body_input])
        return form
