from pytest import mark
import os
import yaml
import re


@mark.smoke
@mark.annotations
class AnnotationsValuesTests:

    @staticmethod
    # TODO: Make a test for every folder (Tests, Framework, Mock, etc..)
    def test_annotations_values(app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP27

        Check the values of annotations from the Framework files.
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

        def extract_annotations(filename):
            """
            :param filename: XAML filename from which we extract annotations for arguments and variables
            :return: List of tuples (annotation, variable/argument, filename)
            """
            argument_variable_re = re.compile('((x:Property|Variable x:TypeArguments=).*)')
            name_re = re.compile('(?<=Name=\")((in|out|io)_[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)')
            annotation_value_re = re.compile('(?<=AnnotationText=\").*?(?=\")')
            annotation_data = []

            with open(filename, "r") as f:
                content = f.read()
                argument_variable_tags = argument_variable_re.findall(content)
                for tag in argument_variable_tags:
                    annotation_value = annotation_value_re.search(tag[0])
                    # Check for NoneType
                    if annotation_value is not None:
                        annotation_value = annotation_value.group(0)

                    name = name_re.search(tag[0]).group(0)

                    split_sep = "VisualBasic" if "VisualBasic" in f.name else "CSharp"
                    annotation_data.append((annotation_value, name, f.name.split(split_sep)[-1].replace("/", "\\")))

            return annotation_data

        def transform_extracted_annotations(extracted_data):
            """
            :param extracted_data: List of tuples (annotation, variable/argument, filename)
            :return: Dictionary similar to the input test file
            """
            transformed_data = {}
            for elem in extracted_data:
                # If the annotation is not yet added
                if elem[0] not in transformed_data:
                    transformed_data[elem[0]] = {}

                # If the argument/variable is not added yet
                if elem[1] not in transformed_data[elem[0]]:
                    transformed_data[elem[0]][elem[1]] = []

                # Populate output
                transformed_data[elem[0]][elem[1]].append(elem[2])  # annotation: {argument/variable: filename}

            return transformed_data

        ''' HERE STARTS THE FUNCTION '''
        # Extracted data that input data is tested against
        extracted_data = []
        extracted_input = {}
        var_to_annot = {}

        # Read input test data
        test_input = yaml.safe_load(
            (open(app_constants.STANDARD_ANNOTATIONS_TEST_DATA, "r"))
        )
        var_to_annot = {v: key for key, value in test_input.items() for v in value}

        # Get path to where the XAMLs are stored
        framework_folder_path = app_constants.PROJECT

        # Iterate through each XAML
        framework_files = get_absolute_filenames(framework_folder_path)
        for framework_file in framework_files:
            extracted_data.extend(extract_annotations(framework_file))
        extracted_input = transform_extracted_annotations(extracted_data)

        test_result = True
        for annotation, variable_filenames in extracted_input.items():
            # If annotation not present in test_input
            if annotation not in test_input:
                print(f"\nWorkflow annotation: {annotation}")
                for variable, filenames in variable_filenames.items():
                    print(f"{variable} - {filenames} -- Expected valued: {var_to_annot.get(variable)}")
                test_result = False

        assert test_result
