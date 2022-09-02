from pytest import fixture
from PythonTests import constants
import json
import xml.etree.ElementTree as ET
import PyPDF2
import yaml


@fixture(scope='function')
def read_file():
    def method(filename):
        """
        Read the Json data
        :param filename: - Path to the file location
        :return: Json Data
        """
        file_content = json.load(open(filename, 'r'))
        return file_content

    return method


@fixture(scope='function')
def convert_to_lower():
    def method(json_file):
        """
        The keys in the two files are not written in the same case, this function corrects this
        :param json_file: the content of the json
        :return: json_file: the content of the json in lower case keys
        """
        json_file = {key.lower() if type(key) == str else key: value for key, value in json_file.items()}
        return json_file

    return method


# function, class, module, package, session
@fixture(scope='function')
def dependency_check(read_file, convert_to_lower):
    def method(proj_json, template_json):
        """
        Compare the "dependencies" field between project and template
        :param proj_json: the content of the project
        :param template_json: the content of the template
        :return: the compare result of the "dependencies" field
        """

        vb_project_json = read_file(proj_json)
        vb_template_json = read_file(template_json)

        vb_project_json = convert_to_lower(vb_project_json)
        vb_template_json = convert_to_lower(vb_template_json)

        return vb_project_json["dependencies"] == vb_template_json["dependencies"]

    return method



"""
for try
"""


def pytest_addoption(parser):
    parser.addoption(
        "--tdata",
        action="store",
        help="test data"
    )


@fixture(scope='session')
def tdata(request):
    return request.config.getoption("--tdata")


"""
end for try
"""

# full path for the test data file for the nuspec test
data_path = 'TestDataGeneration/PythonTests/Nuspec_test_data.yaml'
#data_path = 'TestDataGeneration/PythonTests/UserGuide_test_data.yaml'

def load_test_data(path):
    """
    :param path: The full path of the file containing the test data
    :return: test data
    """
    data = yaml.safe_load((open(path, 'r')))
    return data

@fixture(params=load_test_data(data_path))
def test_data(request):
    data = request.param
    return data


@fixture(scope='function')
def read_xml():
    def method(nuspec_file):
        """
        Read the xml data
        :param nuspec_file: the nuspec file full path
        :return: xml Data
        """

        # Passing the path of the xml document to enable the parsing process
        tree = ET.parse(nuspec_file)

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
        pdfFileObj = open(user_guide_file, 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)

        return pdfReader

    return method

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
