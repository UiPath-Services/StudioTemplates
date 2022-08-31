from pytest import fixture
import json


# function, class, module, package, session
@fixture(scope='function')
def dependency_check(template_json, proj_json):
    vb_project_json = json.load(open(proj_json, 'r'))
    vb_template_json = json.load(open(template_json, 'r'))

    for key, value in vb_project_json.items():
        if type(key) == str:
            vb_project_json[key.lower()] = value
        else:
            vb_project_json[key] = value

    for key, value in vb_template_json.items():
        if type(key) == str:
            vb_template_json[key.lower()] = value
        else:
            vb_template_json[key] = value

    return vb_project_json["dependencies"] == vb_template_json["dependencies"]

