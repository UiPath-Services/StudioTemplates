from pytest import fixture
from constants import Constants

import json
import PyPDF2
import yaml
import xml.etree.ElementTree as et

# Test Data Paths
FOLDER_STRUCTURE_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/FolderStructure_test_data.yaml"
NUSPEC_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/Nuspec_test_data.yaml"
USER_GUIDE_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/UserGuide_test_data.yaml"
PROJECT_JSON_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/Project_Json_test_data.yaml"


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        help="Development language selection between VB/CSharp"
    )


@fixture(scope='session')
def env(request):
    return request.config.getoption("--env")


@fixture(scope='session')
def app_constants(env):
    const = Constants(env)
    return const


def convert_to_lower(json_file):
    """
    The keys in the two files are not written in the same case, this function corrects this
    :param json_file: the content of the json
    :return: json_file: the content of the json in lower case keys
    """
    json_file = {key.lower() if type(key) == str else key: value for key, value in json_file.items()}
    return json_file

# TODO: Move the dependency check to the template test as it is related to that specifically
# function, class, module, package, session
@fixture(scope='function')
def dependency_check():
    def method(proj_json, template_json):
        """
        Compare the "dependencies" field between project and template
        :param proj_json: the content of the project
        :param template_json: the content of the template
        :return: the compare result of the "dependencies" field
        """

        vb_project_json = json.load(open(proj_json, 'r'))
        vb_template_json = json.load(open(template_json, 'r'))

        vb_project_json = convert_to_lower(vb_project_json)
        vb_template_json = convert_to_lower(vb_template_json)

        return vb_project_json["dependencies"] == vb_template_json["dependencies"]

    return method


# @fixture(scope='function')
# def load_test_data():
#
#     def method(path):
#         """
#         :param path: The full path of the file containing the test data
#         :return: test data
#         """
#         data = yaml.safe_load((open(path, 'r')))
#         return data
#
#     return method

# TODO: Let's find a way to make this a fixture
def load_test_data(path):
    """
    :param path: The full path of the file containing the test data
    :return: test data
    """
    data = yaml.safe_load((open(path, 'r')))
    return data


@fixture(params=load_test_data(NUSPEC_TEST_DATA))
def test_data_nuspec(request):
    data = request.param
    return data


@fixture(params=load_test_data(PROJECT_JSON_TEST_DATA))
def test_data_project_json(request):
    data = request.param
    return data


@fixture(params=load_test_data(USER_GUIDE_TEST_DATA))
def test_data_user_guide(request):
    data = request.param
    return data

# TODO: Should we use this than the way it is implemented now?

# @fixture(params=load_test_data(FOLDER_STRUCTURE_TEST_DATA))
# def test_data_folder_structure(request):
#     data = request.param
#     return data


@fixture(scope='function')
def read_xml():
    def method(nuspec_file):
        """
        Read the xml data
        :param nuspec_file: the nuspec file full path
        :return: xml Data
        """

        # Passing the path of the xml document to enable the parsing process
        tree = et.parse(nuspec_file)

        # getting the parent tag of the xml document
        root = tree.getroot()

        return root

    return method


@fixture(scope='function')
def read_pdf():
    def method(user_guide_file):
        """
        Read the User Guide data
        :param user_guide_file: The User Guide file full path
        :return: pdf Data
        """

        # creating a pdf file object
        pdf_file_obj = open(user_guide_file, 'rb')

        # creating a pdf reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

        return pdf_reader

    return method

# TODO: This should move to the actual test
@fixture(scope='function')
def compare_config():
    def method(project_config, expected_config):
        """
        :param project_config: the content of the Config.xlsx
        :param expected_config: the expected content of the Config.xlsx
        :return: comparison result
        """

        for key in expected_config.keys():
            if not expected_config[key].equals(project_config[key]):
                return False
        return True

    return method
