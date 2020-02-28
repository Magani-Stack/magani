import json
import os
import magani


def read_project_file():
    try:
        f = "{}/{}".format(os.path.abspath(os.path.dirname(magani.__file__)), "data/projects/projects.json")
        print(f)
        file_data = open(f, "r").read()
        if file_data:
            return eval(file_data, {"null": None})
        else:
            return []
    except Exception as e:
        print(e)
        return []


def write_project_file(projects):
    fw = "{}/{}".format(os.path.abspath(os.path.dirname(magani.__file__)), "data/projects/projects.json")
    print(fw)
    with open(fw, "w") as f:
        f.writelines(json.dumps(projects, indent=4, sort_keys=True, default=lambda x: str(x)))
        f.write("\n")

    return True


if __name__ == "__main__":
    print(os.path)
