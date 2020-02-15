import json


def read_project_file():
    file_data = open("data/projects/projects.json", "r").read()
    if file_data:
        return eval(file_data, {"null": None})
    else:
        return []


def write_project_file(projects):
    with open("data/projects/projects.json", "w") as f:
        f.writelines(json.dumps(projects, indent=4, sort_keys=True, default=lambda x: str(x)))
        f.write("\n")

    return True
