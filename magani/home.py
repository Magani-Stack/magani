import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import json
from magani_server import app
from magani.utils.card_util import CreateProjectCard
from magani.utils.file_util import read_project_file, write_project_file


def project_list():
    projects = read_project_file()
    list_of_projects = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        CreateProjectCard(x["Project"], x["Description"]).get()
                    ],
                    width="auto"
                )
            ]

        )

        for x in projects
    ]
    return html.Div(
        list_of_projects
    )


email_input = dbc.Form(
    [
        dbc.Label("Project Name", html_for="Contact_Email_Id"),
        dbc.Input(type="text", id="Create_Project_Name_ID", placeholder="Enter the project name"),
    ]
)

message_input = dbc.Form(
    [
        dbc.Label("Project Description", html_for="Create_Project_Description_Id"),
        dbc.Textarea(
            id="Create_Project_Description_Id",
            placeholder="Enter the project description",
        )
    ]
)

form = dbc.Form([email_input, message_input])

create_modal = dbc.Modal(
    [
        dbc.ModalHeader("Create New Project"),
        dbc.ModalBody([
            form
        ]),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Create", id="Create_Project_Submit_ID", className="ml-auto", n_clicks=0, disabled=True
                )
            ]
        ),
    ],
    id="Create_Modal_ID",
    centered=True,
)


def create_project():
    return html.Div([
        dbc.Button("Create Project", id="Create_Project_ID"),
        create_modal
    ],
        style={"text-align": "center", "margin-bottom": "32px"})


def layout():
    return dbc.Container(
        [
            create_project(),
            project_list()

        ]
    )


@app.callback(Output('Create_Project_Submit_ID', 'disabled'),
              [Input("Create_Project_Name_ID", "value"), Input("Create_Project_Description_Id", "value")])
def create_project_submit_btn_update(email, message):
    if email and message:
        return False
    return True


@app.callback(
    Output("Create_Modal_ID", "is_open"),
    [Input("Create_Project_ID", "n_clicks"), Input('Create_Project_Submit_ID', 'n_clicks')],
    [State("Create_Modal_ID", "is_open"),
     State("Create_Project_Name_ID", "value"),
     State("Create_Project_Description_Id", "value")],
)
def toggle_modal(n1, n2, is_open, project, description):
    print(n1, n2)
    if n1 or n2:
        if project and description:
            print(project, description)
            projects = read_project_file()
            p = {
                "Project": project,
                "Description": description,
                "TestCase": []
            }
            projects.append(p)
            write_project_file(projects)
        return not is_open
    return is_open
