import dash_bootstrap_components as dbc
from dash import html


class CreateCard:

    def __init__(self):
        self.card = None

    def get(self):
        return self.card


class CreateProjectCard(CreateCard):

    def __init__(self, project_name, description):
        super().__init__()
        self.card = html.A(html.Button(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Project : {}".format(project_name), className="card-title"),
                        html.H6("Description : {}".format(description), className="card-subtitle",
                                style={"margin-bottom": "8px"}),
                        html.Div([
                            dbc.CardLink(dbc.Button("Test", style={"margin-right": "16px"}, color="primary"),
                                         href="{}/test".format(project_name), style={"float": "left"}),
                            # dbc.CardLink(dbc.Button("Open", style={"margin-right": "20px"}, color="info"),
                            #              href=project_name),
                            html.A(dbc.Button("Export CSV", style={"margin-right": "32px"}, color="secondary"),
                                   href="{}/export/csv".format(project_name)),
                            html.A(dbc.Button("Export Excel", style={"margin-right": "32px"}, color="secondary"),
                                   href="{}/export/excel".format(project_name)),
                            dbc.CardLink(dbc.Button("Delete", color="danger", style={"margin-right": "16px"}),
                                         href="{}/delete".format(project_name), style={"float": "right"}),
                            # dbc.Badge("Success", style={"float": "right"})
                        ], )
                    ]
                ),
                style={"width": "65rem"},
            )
        ), href=project_name
        )


class CreateTestCard(CreateCard):

    def __init__(self, project, api, api_id, method, status):
        super().__init__()
        print("status", status)
        status_color = "success" if "success" == status.lower() else "danger"
        self.card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4("API : {}".format(api), className="card-title"),
                    html.H6("Method : {}".format(method), className="card-subtitle"),
                    html.Div([
                        dbc.CardLink(dbc.Button("Test", style={"margin-right": "16px"}, color="primary"),
                                     href="{}/{}/test".format(project, api_id)),
                        dbc.CardLink(dbc.Button("Delete", color="danger", style={"margin-right": "16px"}),
                                     href="{}/{}/delete".format(project, api_id), style={"float": "right"}),
                        dbc.Badge(status, color=status_color, style={"float": "center"})
                    ], )
                ]
            ),
            style={"width": "20rem"},
        )
