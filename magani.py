from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from config import APP_TITLE_NAME, SUB_TITLE_NAME
from magani import home, project, run_test_case, delete_test_case
from server import app

header = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("mg.jpg"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                # "margin-bottom": "25px",
                            },
                        ),
                        href="/"),

                ],
                width=2
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.H1(
                                APP_TITLE_NAME,
                                style={"margin-bottom": "0px"},
                            ),
                            html.H5(
                                SUB_TITLE_NAME, style={"margin-top": "0px"}
                            ),
                        ]
                    )
                ],
                width=8
            ),
            dbc.Col(
                [
                    # html.Div(
                    #     [
                    #         html.A(
                    #             html.Button("Contact Us", id="learn-more-button"),
                    #             href="#",
                    #             target="_blank",
                    #         )
                    #     ],
                    #     className="float-right"
                    # )
                ],
                width=2
            ),
        ]
    ),
    className="bg-info",
    style={"max-width": "100%"}
)

email_input = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="Contact_Email_Id"),
        dbc.Input(type="email", id="Contact_Email_Id", placeholder="Enter Your Email"),
    ]
)

message_input = dbc.FormGroup(
    [
        dbc.Label("Message", html_for="Contact_Message_Id"),
        dbc.Textarea(
            # type="text",
            id="Contact_Message_Id",
            placeholder="Enter Message You Wish To Share With Us",
        )
    ]
)

form = dbc.Form([email_input, message_input])

modal = html.Div(
    [
        dbc.Button("ContactUS", id="open-centered"),
        dbc.Modal(
            [
                dbc.ModalHeader("Send Message"),
                dbc.ModalBody([
                    form
                ]),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Submit", id="submit-centered", className="ml-auto", n_clicks=0, disabled=True
                        )
                    ]
                ),
            ],
            id="modal-centered",
            centered=True,
        ),
    ]
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.P("Copyright © 2020 Magani. All rights reserved.")
                ]
            ),
            dbc.Col(
                [
                    # html.P("Company information"),
                    modal
                ]
            ),
        ]
    ),
    # style={"margin-top": "30%"}
)

app.layout = html.Div(
    [
        header,
        html.Br(style={'padding': 10}),
        html.Div(
            [
                html.Div(
                    html.Div(id='page-content', className='content'),
                    className='content-container',
                ),
            ],
            className='container-width',
            style={"width": "100%"}
        ),
        dcc.Location(id='url', refresh=False),
        html.Br(style={'padding': 10}),
        footer
    ],
    style={"width": "100%"}
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print("path : ", pathname, type(pathname))
    print(pathname and len(str(pathname).split("/")) == 2)

    paths = pathname.split("/") if pathname else pathname
    print("path list", paths)
    if pathname == '/':
        return home.layout()
    elif pathname and len(str(pathname).split("/")) == 2:
        return project.layout(pathname.strip("/").split("/")[0])
    elif pathname and len(str(pathname).split("/")) in [3, 4]:
        if str(pathname).split("/")[-1] == "delete":
            return delete_test_case.layout(pathname)
        elif str(pathname).split("/")[-1] == "test":
            return run_test_case.layout(pathname)
        # elif str(pathname).split("/")[-1] == "test":
        #     return
    else:
        return dbc.Container([html.H1("404")])


@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input('submit-centered', 'n_clicks')],
    [State("modal-centered", "is_open"), State("Contact_Email_Id", "value"), State("Contact_Message_Id", "value")],
)
def toggle_modal(n1, n2, is_open, email, message):
    print(n1, n2)
    if n1 or n2:
        if email and message:
            f_n = str(datetime.now()).replace(":", "_").replace(" ", "_").replace("-", "_")
            with open("contacts/{}.txt".format(f_n), "w") as f:
                f.write("Email : {}".format(email))
                f.writelines("\n")
                f.writelines("Message : {}".format(message))
                f.writelines("\n")
        return not is_open
    return is_open


@app.callback(Output('submit-centered', 'disabled'),
              [Input("Contact_Email_Id", "value"), Input("Contact_Message_Id", "value")])
def submit_btn_update(email, message):
    if email and message:
        return False
    return True


if __name__ == '__main__':
    app.run_server()
