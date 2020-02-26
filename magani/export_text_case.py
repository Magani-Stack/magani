import io
from datetime import datetime

import pandas as pd
from flask import send_file

from magani.utils.file_util import read_project_file


def layout(project):
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


if __name__ == "__main__":
    layout("Google")
