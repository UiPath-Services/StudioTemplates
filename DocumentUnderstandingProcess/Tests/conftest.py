from pytest import fixture


# function, class, module, package, session
@fixture(scope='function')
def dependency_check(template_json, proj_json):
    print("I have done the dependency check")
    return True

