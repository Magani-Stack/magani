import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
from server import app


def project_list():
    projects = eval(open("data/projects/projects.json", "r").read())
    i = 3
    list_of_projects = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Project : {}".format(x["Project"]), className="card-title"),
                                    html.H6("Description : {}".format(x["Description"]), className="card-subtitle"),
                                    html.Div(
                                        [
                                            dbc.Button("Test", style={"margin-right": "16px"}),
                                            dbc.Button("Open", style={"margin-right": "16px"}),
                                            dbc.Button("Delete", style={"margin-right": "16px"}),
                                            dbc.Badge("Success", style={"float": "right"})
                                        ],
                                    )
                                ]
                            ),
                            style={"width": "65rem"},
                        )
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


email_input = dbc.FormGroup(
    [
        dbc.Label("Project Name", html_for="Contact_Email_Id"),
        dbc.Input(type="text", id="Create_Project_Name_ID", placeholder="Enter the project name"),
    ]
)

message_input = dbc.FormGroup(
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
    ])


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
            projects = eval(open("data/projects/projects.json", "r").read())
            p = {
                "Project": project,
                "Description": description
            }
            projects.append(p)
            with open("data/projects/projects.json", "w") as f:
                f.writelines(json.dumps(projects, indent=4, sort_keys=True))
                f.write("\n")
        return not is_open
    return is_open
