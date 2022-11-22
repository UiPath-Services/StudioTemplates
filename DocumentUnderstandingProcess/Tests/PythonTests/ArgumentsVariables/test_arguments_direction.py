from pytest import mark
import os
import yaml
import re

@mark.smoke
@mark.arguments
class ArgumentsDirectionTests:
    @staticmethod
    def test_arguments_direction(app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP45

        Check that all arguments have the correct direction set.
        """

        def get_absolute_filenames(path):
            """
            Returns the full paths of the files found in a given folder.
            :param path: The full path of the folder containing the data
            :return: List of absolute filenames
            """
            absolute_filenames = []
            for root, _, files in os.walk(path):
                for file in files:
                    if file.split(".")[-1].lower() != "xaml":
                        continue
                    absolute_filenames.append(os.path.join(root, file))
            return absolute_filenames

        def extract_argument_direction(filename):
            """
            :param filename: XAML filename from which we extract annotations for arguments and variables
            :return: List of tuples (filename, argument, direction)
            """

            """ 
            Python's re. compile() method is used to compile a regular expression pattern provided as a string into 
            a regex pattern object ( re. Pattern ). Later we can use this pattern object to search for a match 
            inside different target strings using regex methods such as a re.
            """
            # Regex for argument
            argument_re = re.compile('((x:Property).*)')
            # Regex for arguments name
            name_re = re.compile('(?<=Name=\")((in|out|io)_[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)')
            # Regex for arguments type
            type_value_re = re.compile('(?<=Type=\").*?(?=\")')
            # the list of tuples
            annotation_data = []

            with open(filename, "r") as f:
                content = f.read()
                argument_variable_tags = argument_re.findall(content)
                for tag in argument_variable_tags:
                    direction_value = type_value_re.search(tag[0])
                    # Check for NoneType
                    if direction_value is not None:
                        direction_value = direction_value.group(0)

                    name = name_re.search(tag[0]).group(0)

                    annotation_data.append((os.path.basename(f.name), name, direction_value))

            return annotation_data

        def transform_extracted_arguments(extracted_data):
            """
            :param extracted_data: List of tuples (filename, argument, direction)
            :return: Dictionary similar to the input test file 
                {'filename1': {'argument1': 'direction1', 'argument2': 'direction2'}, 'filename2': {...}}
            """
            transformed_data = {}
            for elem in extracted_data:
                # If the annotation is not yet added
                if elem[0] not in transformed_data:
                    transformed_data[elem[0]] = {}

                # If the argument is not added yet
                if elem[1] not in transformed_data[elem[0]]:
                    transformed_data[elem[0]][elem[1]] = {}

                # delete the last part of the elem[2], so that only the direction (type) remains.
                # eg. instead of OutArgument(x:String) remain with OutArgument
                # Populate output
                transformed_data[elem[0]][elem[1]] = elem[2][:elem[2].index("(")]  # filename: {argument: direction}

            return transformed_data

        ''' HERE STARTS THE FUNCTION '''
        # Extracted data that input data is tested against
        extracted_data = []
        extracted_input = {}
        var_to_annot = {}

        # Read input test data
        test_input = yaml.safe_load(
            (open(app_constants.ARGUMENTS_DIRECTION_TEST_DATA, "r"))
        )

        # Get path to where the XAMLs are stored
        framework_folder_path = app_constants.PROJECT

        # Iterate through each XAML
        framework_files = get_absolute_filenames(framework_folder_path)
        for framework_file in framework_files:
            # The extend() method adds all the elements of an iterable (list, tuple, string etc.) to the end of the list
            extracted_data.extend(extract_argument_direction(framework_file))
        # transform from (filename1, argument1, direction1), (filename1, argument2, direction2), (filename2,..)
        # to {'filename1': {'argument1': 'direction1', 'argument2': 'direction2'}, 'filename2': {...}}
        extracted_input = transform_extracted_arguments(extracted_data)

        # check that all the arguments from the test input file are present and with the correct direction in the workflow
        test_result = True
        for filename, argument_and_direction in test_input.items():
            if filename in extracted_input:
                for argument, direction in argument_and_direction.items():
                    if argument in extracted_input[filename]:
                        if direction != extracted_input[filename][argument]:
                            test_result = False
                            print(f"\nFile {filename}")
                            print(f"Expected: argument {argument} has {direction} direction.")
                            print(f"Workflow: argument {argument} has {extracted_input[filename][argument]} direction.")
                    else:
                        test_result = False
                        print(f"\nFile {filename}")
                        print(f"Expected: argument {argument} is present in file.")
                        print(f"Workflow: argument {argument} is not present in file.")
            else:
                test_result = False
                print(f"\nFile {filename}")
                print(f"Expected: file to have these arguments {argument_and_direction}")
                print(f"Workflow: file has no arguments.")

        # check that all the arguments from the workflow are present in the test input file
        for filename, argument_and_direction in extracted_input.items():
            if filename in test_input:
                for argument, direction in argument_and_direction.items():
                    if argument not in test_input[filename]:
                        test_result = False
                        print(f"\nFile {filename}")
                        print(f"Expected: argument {argument} is not present in file.")
                        print(f"Workflow: argument {argument} is present in file.")
            else:
                test_result = False
                print(f"\nFile {filename}")
                print(f"Expected: file to not have arguments.")
                print(f"Workflow: file has these arguments {argument_and_direction}.")

        assert test_result
