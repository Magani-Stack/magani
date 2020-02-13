import json


def read_project_file():
    return eval(open("data/projects/projects.json", "r").read(), {"null": None})


def write_project_file(projects):
    with open("data/projects/projects.json", "w") as f:
        f.writelines(json.dumps(projects, indent=4, sort_keys=True))
        f.write("\n")

    return True
