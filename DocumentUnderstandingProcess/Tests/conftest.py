from pytest import fixture
from constants import Constants

import json
import yaml
import pypdf
import os
import xml.etree.ElementTree as et

# Test Data Paths
ROOT_TEST_DATA_VARIATION = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/"
DATA_FOLDER_STRUCTURE_TEST_DATA = ROOT_TEST_DATA_VARIATION + "DataFolderStructure_test_data.yaml"
NUSPEC_TEST_DATA = ROOT_TEST_DATA_VARIATION + "Nuspec_test_data.yaml"
USER_GUIDE_TEST_DATA = ROOT_TEST_DATA_VARIATION + "UserGuide_test_data.yaml"
PROJECT_JSON_TEST_DATA = ROOT_TEST_DATA_VARIATION + "Project_Json_test_data.yaml"

# Dictionary used for the test parametrization hook
TEST_DATA_MAPPING = {
    "test_data_folder_structure": DATA_FOLDER_STRUCTURE_TEST_DATA,
    "test_data_folder_content": DATA_FOLDER_STRUCTURE_TEST_DATA,
    "test_nuspec_version_as_expected": NUSPEC_TEST_DATA,
    "test_user_guide_version_as_expected": USER_GUIDE_TEST_DATA,
    "test_project_json_variation_path": PROJECT_JSON_TEST_DATA,
}


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", help="Development language selection between VB/CSharp"
    )


@fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@fixture(scope="session")
def app_constants(env):
    const = Constants(env)
    return const


@fixture(scope="function")
def convert_to_lower():
    """
    The keys in the two files are not written in the same case, this function corrects this
    :param json_file: the content of the json
    :return: json_file: the content of the json in lower case keys
    """

    def method(json_file):
        json_file = {
            key.lower() if type(key) == str else key: value
            for key, value in json_file.items()
        }
        return json_file

    return method


@fixture(scope="function")
def load_json():
    """
    :param path: The full path of the file containing the data
    :return: data
    """

    def method(path):
        data = json.load((open(path, "r")))
        return data

    return method


def pytest_generate_tests(metafunc):
    """
    Pytest hook that generates parametrized calls to given test functions
    :param metafunc: Object that helps with test function inspection and test generation
    :return:
    """
    test_name_list = [test_name for test_name in TEST_DATA_MAPPING.keys()]
    test_name = metafunc.function.__name__

    if test_name in test_name_list:
        data = yaml.safe_load((open(TEST_DATA_MAPPING[test_name], "r")))
        metafunc.parametrize("test_data", data)


@fixture(scope="function")
def load_test_input():
    """
    :param path: The full path of the file containing the test input
    :return: test data
    """

    def method(path):
        data = yaml.safe_load((open(path, "r")))
        return data

    return method


@fixture(scope="function")
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


@fixture(scope="function")
def read_pdf():
    def method(user_guide_file):
        """
        Read the User Guide data
        :param user_guide_file: The User Guide file full path
        :return: pdf Data
        """

        # creating a pdf file object
        pdf_file_obj = open(user_guide_file, "rb")

        # creating a pdf reader object
        pdf_reader = pypdf.PdfReader(pdf_file_obj)

        return pdf_reader

    return method


@fixture(scope="function")
def get_filenames():
    """
    :param path: The full path of the file containing the data
    :return: List with all the xaml file names
    """

    def method(path):
        filenames = []
        for _, _, files in os.walk(path):
            for name in files:
                if name.split(".")[-1].lower() != "xaml":
                    continue
                filenames.append(name)
        return filenames

    return method


@fixture(scope="function")
def get_absolute_filenames():
    """
    Returns the full paths of the files found in a given folder.
    :param path: The full path of the folder containing the data
    :return: List of absolute filenames
    """

    def method(path):
        absolute_filenames = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.split(".")[-1].lower() != "xaml":
                    continue
                absolute_filenames.append(os.path.join(root, file))
        return absolute_filenames

    return method

@fixture(scope="function")
def retry_interval():
    """
    :param filename: XAML filename in which we search for presence of retry scope activity and RetryInterval property
           retry_scope_re: regular expression pattern object to search for Retry Scope
           retry_property_re: regular expression pattern object to search for Property
           retry_property_value_re: regular expression pattern object to search for Property value
    :return: True - the file does not have a retry scope activity
             True - the file has retry scope activity and the property is configurable
             False - the file has retry scope activity, but the property is not configurable
    """

    def method(filename, retry_scope_re, retry_property_re, retry_property_value_re):
        digit_found = False

        with open(filename, "r") as f:
            content = f.read()
            retry_scope_tags = retry_scope_re.findall(content)
            for tag in retry_scope_tags:
                retry_property_value = retry_property_re.search(tag[0])
                # Check for NoneType
                if retry_property_value is not None:
                    retry_property_value = retry_property_value.group(0)
                    # check if value is configurable or hard coded
                    if retry_property_value_re.search(retry_property_value) != None:
                        print("\nFile " + filename + " has a retry scope with hard coded property")
                        digit_found = True

        return not digit_found

    return method

@fixture(scope="function")
def extract_argument_direction():
    """
    :param filename: XAML filename from which we extract the direction of arguments
           argument_re: regular expression pattern object to search for argument
           name_re: regular expression pattern object to search for argument name
           type_value_re: regular expression pattern object to search for argument direction
    :return: List of tuples (filename, argument, direction)
    """

    def method(filename, argument_re, name_re, type_value_re):

        # the list of tuples
        argument_data = []

        with open(filename, "r") as f:
            content = f.read()
            argument_variable_tags = argument_re.findall(content)
            for tag in argument_variable_tags:
                direction_value = type_value_re.search(tag[0])
                # Check for NoneType
                if direction_value is not None:
                    direction_value = direction_value.group(0)

                name = name_re.search(tag[0]).group(0)

                argument_data.append((os.path.basename(f.name), name, direction_value))
        return argument_data

    return method
