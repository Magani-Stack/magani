import dash_bootstrap_components as dbc
import dash_html_components as html


class CreateCard:

    def __init__(self):
        self.card = None

    def get(self):
        return self.card


class CreateProjectCard(CreateCard):

    def __init__(self, project_name, description):
        super().__init__()
        self.card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Project : {}".format(project_name), className="card-title"),
                    html.H6("Description : {}".format(description), className="card-subtitle"),
                    html.Div([
                        dbc.CardLink(dbc.Button("Test", style={"margin-right": "16px"}),
                                     href="{}/test".format(project_name)),
                        dbc.CardLink(dbc.Button("Open", style={"margin-right": "16px"}), href=project_name),
                        dbc.CardLink(dbc.Button("Delete", style={"margin-right": "16px"}),
                                     href="{}/delete".format(project_name)),
                        # dbc.Badge("Success", style={"float": "right"})
                    ], )
                ]
            ),
            style={"width": "65rem"},
        )


class CreateTestCard(CreateCard):

    def __init__(self, project, api, api_id, method, status):
        super().__init__()
        print("status", status)
        self.card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4("API : {}".format(api), className="card-title"),
                    html.H6("Method : {}".format(method), className="card-subtitle"),
                    html.Div([
                        dbc.CardLink(dbc.Button("Test", style={"margin-right": "16px"}),
                                     href="{}/{}/test".format(project, api_id)),
                        dbc.CardLink(dbc.Button("Delete", style={"margin-right": "16px"}),
                                     href="{}/{}/delete".format(project, api_id)),
                        # dbc.Badge(status, color="success", style={"float": "right"})
                    ], )
                ]
            ),
            style={"width": "20rem"},
        )
