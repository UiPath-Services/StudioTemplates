from pytest import fixture
from constants import Constants

import json
import PyPDF2
import yaml
import os
import xml.etree.ElementTree as et

# Test Data Paths
DATA_FOLDER_STRUCTURE_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/DataFolderStructure_test_data.yaml"
NUSPEC_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/Nuspec_test_data.yaml"
USER_GUIDE_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/UserGuide_test_data.yaml"
PROJECT_JSON_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/Project_Json_test_data.yaml"


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

@fixture(scope='function')
def convert_to_lower():
    """
    The keys in the two files are not written in the same case, this function corrects this
    :param json_file: the content of the json
    :return: json_file: the content of the json in lower case keys
    """

    def method(json_file):
        json_file = {key.lower() if type(key) == str else key: value for key, value in json_file.items()}
        return json_file

    return method


@fixture(scope='function')
def load_json():
    """
    :param path: The full path of the file containing the data
    :return: data
    """
    def method(path):
        data = json.load((open(path, 'r')))
        return data
    return method


# TODO: Let's find a way to make this a fixtue
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


@fixture(params=load_test_data(DATA_FOLDER_STRUCTURE_TEST_DATA))
def test_data_folder(request):
    data = request.param
    return data


@fixture(scope='function')
def load_test_input():
    """
    :param path: The full path of the file containing the test input
    :return: test data
    """
    def method(path):
        data = yaml.safe_load((open(path, 'r')))
        return data
    return method


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


@fixture(scope='function')
def get_filenames():
    """
    :param path: The full path of the file containing the data
    :return: data
    """
    def method(path):
        filenames = []
        for _, _, files in os.walk(path + "Framework"):
            for name in files:
                filenames.append(name)
        return filenames

    return method
