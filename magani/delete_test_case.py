import dash_bootstrap_components as dbc
from dash import html

from magani.utils.file_util import read_project_file, write_project_file


def layout(pathname):
    lt = str(pathname).strip("/").split("/")
    project = lt[0]
    action = lt[-1]
    api_id = lt[1] if len(lt) == 3 else None

    projects_new = read_project_file()
    projects_delete = [x for x in projects_new if x["Project"] == project]

    print("{} action for project {}".format(action, project))
    if action == "delete":
        for pr in projects_delete:
            projects_new.remove(pr)
        if api_id:
            apis = [y for x in projects_delete for y in x["TestCase"] if y["ID"] == api_id]
            for api in apis:
                projects_delete[0]["TestCase"].remove(api)

            projects_new.extend(projects_delete)
            write_project_file(projects_new)
            return dbc.Container(
                [
                    html.H1("Deleted Test Case from {} ".format(project))
                ]
            )

        write_project_file(projects_new)

        print("deleted {} ".format(project))
        return dbc.Container(
            [
                html.H1("Deleted project {} ".format(project))
            ]
        )
