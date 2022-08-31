import yaml
import json
import os


def read_yaml(filename):
    """
    Read the Yaml data.
    :param filename: - Path to the file location
    :return: Yaml data
    """
    return yaml.safe_load((open(filename, 'r')))


def read_json(filename):
    """
    Read the Json data
    :param filename: - Path to the file location
    :return: Json Data
    """
    return json.load(open(filename, 'r'))


def generate_config_file(data):
    """
    Generates the config file in the .variations folder
    :param data: Yaml Data Object
    :return: config file to be written to disk
    """
    # Create an empty list, which is the inside of the config dictionary
    inside_config = []

    # For each test case in the yaml object, append to the list 'inside_config' the corresponding dict
    # Finally add the list of dictionaries to the main config file
    for testcase in data["TestCaseDataGeneration"]:
        inside_config.append({"filePath": ".variations\\" + testcase + ".json", "dataVariationType": "File"})
    config = {"dataVariationFileInfo": inside_config}
    return config


def generate_test_variation(data, testcase):
    """
    Generates a json file with the test data variation based on the yaml template
    :param data: Yaml Data Object
    :param testcase: TestCase for which we'll make the test data file
    :return: Test Variation list. To be Written to a json file
    """

    """
    Output example of the function 
    [
        {"in_ReleaseVersion": "22.10-preview17", "in_ExpectedResult": "failed"}, 
        {"in_ReleaseVersion": "22.10", "in_ExpectedResult": "passed"}, 
        {"in_ReleaseVersion": "22.6", "in_ExpectedResult": "failed"}
    ]
    """

    yaml_testcase_dict = data["TestCaseDataGeneration"][testcase]
    list_of_keys = list(yaml_testcase_dict.keys())

    # Create an empty list of dictionaries which will then be populated by all the options in the Yaml Test Data File
    test_datasets = [{} for _ in range(len(yaml_testcase_dict[list_of_keys[0]]))]

    """
    Populate the list of dictionaries
    list_index = the index in the list
    argument = dictionary key
    data_point = dictionary value
    """
    for argument in yaml_testcase_dict:
        list_index = 0
        for data_point in yaml_testcase_dict[argument]:
            test_datasets[list_index][argument] = data_point
            list_index += 1

    return test_datasets


def update_project_file(json_data, yaml_data):
    """
    Updates the Project File to contain the Data Variation File Paths
    :param json_data: Json Object to be modified
    :param yaml_data: Yaml Object to be read
    :return: Json Object to be written
    """
    # We're generating a list of all the test cases
    testcases = list(yaml_data["TestCaseDataGeneration"])

    # We're going through each element in the list and searching for the testcases we have.
    # If we find a match, we add a new Key Value pair at that location
    # I know this needs optimization. Let future Sergiu handle it.
    for element in json_data["designOptions"]["fileInfoCollection"]:
        for testcase in testcases:
            if testcase in element["fileName"]:
                element["dataVariationFilePath"] = ".variations\\" + testcase + ".json"
    return json_data


def write_json_file(data, path, filename):
    """
    Writes Json Files to disk based on the data given and the path selected in the save location param
    :param data: Json Data to be saved to disk
    :param path: Path where to save the data
    :param filename: Filename to be given to the Json Dump
    :return: None
    """
    # Go to the correct path and generate the file
    full_file_path = path + "/" + filename
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

    with open(full_file_path, 'w') as out_file:
        json.dump(data, out_file)


# Location where we'll save the config and test data files we create for VB
vb_save_location_project = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/"
vb_save_location_config = vb_save_location_project + ".variations/"

# Location where we'll save the config and test data files we create for C#
csharp_save_location_project = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/Csharp/"
csharp_save_location_config = csharp_save_location_project + ".variations/"

# Read Data
test_data = read_yaml(
    "../../../DocumentUnderstandingProcess/Tests/TestDataGeneration/DocumentUnderstandingTestData.yaml")
vb_project_json = read_json(vb_save_location_project + "project.json")
csharp_project_json = read_json(csharp_save_location_project + "project.json")

# Config File Generation
config_file = generate_config_file(test_data)
write_json_file(config_file, vb_save_location_config, "config.json")
write_json_file(config_file, csharp_save_location_config, "config.json")

# Test Variation File Generation
for test in test_data["TestCaseDataGeneration"]:
    test_variation_data = generate_test_variation(test_data, test)
    write_json_file(test_variation_data, vb_save_location_config, test + ".json")
    write_json_file(test_variation_data, csharp_save_location_config, test + ".json")


# Project File Update with Test Variation Data VB
vb_project_json = update_project_file(vb_project_json, test_data)
write_json_file(vb_project_json, vb_save_location_project, "project.json")

# Project File Update with Test Variation Data CSharp
csharp_project_json = update_project_file(csharp_project_json, test_data)
write_json_file(csharp_project_json, csharp_save_location_project, "project.json")
