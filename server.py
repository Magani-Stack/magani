import dash
import dash_bootstrap_components as dbc

from config import APP_TITLE_NAME

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=[
        {
            "src": "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js",
            "data-ad-client": "ca-pub-1508089654065875"
        }
    ]
)
server = app.server
app.title = APP_TITLE_NAME
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False
