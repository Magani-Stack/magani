import io
from datetime import datetime

import pandas as pd
from flask import send_file
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from magani.utils.file_util import read_project_file

FILE_FORMATS = ["csv", "excel"]


def export_excel(df: pd.DataFrame, project: str):
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer)
    excel_buffer.seek(0)
    time_str = str(datetime.now()).replace("-", "_").replace(":", "_").replace(" ", "_").replace(".", "_")
    file_name = "{}_{}.xlsx".format(project, time_str)
    return send_file(excel_buffer, mimetype='application/vnd.ms-excel', attachment_filename=file_name,
                     as_attachment=True)


def export_csv(df: pd.DataFrame, project: str):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer)
    str_io = io.StringIO()
    str_io.writelines(csv_buffer.getvalue())
    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()
    time_str = str(datetime.now()).replace("-", "_").replace(":", "_").replace(" ", "_").replace(".", "_")
    file_name = "{}_{}.csv".format(project, time_str)
    return send_file(mem, mimetype='text/csv', attachment_filename=file_name, as_attachment=True)


def layout(project, format_type):
    # lt = str(pathname).strip("/").split("/")
    # project = lt[0]
    # action = lt[-1]
    # api_id = lt[1] if len(lt) == 3 else None
    # print(api_id)
    # if not (action == "export"):
    #     return

    json_data = read_project_file()
    prj = [p for p in json_data if p["Project"] == project][0]
    lt = []

    for t in prj["TestCase"]:
        t["Project"] = prj["Project"]
        t["Description"] = prj["Description"]
        lt.append(t)

    df = pd.DataFrame(lt)
    df.set_index(["Project"], inplace=True)
    print(df)
    if format_type == "csv":
        return export_csv(df, project)
    else:
        return export_excel(df, project)


def invalid_file_format_html():
    return dbc.Container([
        html.H1("Invalid File Format")
    ])


if __name__ == "__main__":
    layout("Google", "")
