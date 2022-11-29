from pytest import fixture, mark
from constants import Constants

import json
import PyPDF2
import yaml
import os
import xml.etree.ElementTree as et


def return_test_data_location():
    # Test Data Paths
    root_test_data_variation = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataVariation/"
    data_folder_structure_test_data = root_test_data_variation + "DataFolderStructure_test_data.yaml"
    nuspec_test_data = root_test_data_variation + "Nuspec_test_data.yaml"
    user_guide_test_data = root_test_data_variation + "UserGuide_test_data.yaml"
    project_json_test_data = root_test_data_variation + "Project_Json_test_data.yaml"

    test_data_mapping = {
        "test_data_folder_structure": data_folder_structure_test_data,
        "test_data_folder_content": data_folder_structure_test_data,
        "test_nuspec_version_as_expected": nuspec_test_data,
        "test_user_guide_version_as_expected": user_guide_test_data,
        "test_project_json_variation_path": project_json_test_data,
    }
    return test_data_mapping


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
    mappings = return_test_data_location()
    test_name_list = [test_name for test_name in mappings.keys()]
    test_name = metafunc.function.__name__

    if test_name in test_name_list:
        data = yaml.safe_load((open(mappings[test_name], "r")))
        metafunc.parametrize("test_data", data)


# TODO: Let's find a way to make this a fixture
# @fixture(scope="function")
# def load_test_data(request):
#     """
#     :param path: The full path of the file containing the test data
#     :return: test data
#     """
#     mappings = return_test_data_location()
#     data = yaml.safe_load((open(mappings[request.node.originalname], "r")))
#     return data


# @fixture(params=[load_test_data(NUSPEC_TEST_DATA),
#                  load_test_data(PROJECT_JSON_TEST_DATA),
#                  load_test_data(USER_GUIDE_TEST_DATA),
#                  load_test_data(DATA_FOLDER_STRUCTURE_TEST_DATA)])
# def test_data(request):
#     data = request.param
#     return data

# @pytest.fixture
# def thing(request, db):
#     class ThingFactory(object):
#         def get(self):
#             thing = MyModel.objects.create()
#             request.addfinalizer(thing.delete)
#             return thing
#     return ThingFactory()
# @fixture(scope='function')
# def get_test_data(request):
#     class DataFactory(object):
#         @staticmethod
#         def load_data(path):
#             data = yaml.safe_load((open(path, 'r')))
#             request.addfinalizer(data)
#             return get_test_data
#     return DataFactory


# @fixture(params=load_test_data(NUSPEC_TEST_DATA))
# def get_test_data_nuspec(request):
#     data = request.param
#     return data
#
#
# @fixture(params=load_test_data(PROJECT_JSON_TEST_DATA))
# def get_test_data_project_json(request):
#     data = request.param
#     return data
#
#
# @fixture(params=load_test_data(USER_GUIDE_TEST_DATA))
# def get_test_data_user_guide(request):
#     data = request.param
#     return data
#
#
# @fixture(params=load_test_data(DATA_FOLDER_STRUCTURE_TEST_DATA))
# def get_test_data_folder(request):
#     data = request.param
#     return data


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
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

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
