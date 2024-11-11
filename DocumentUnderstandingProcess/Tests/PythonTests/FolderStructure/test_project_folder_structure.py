from pytest import mark
import os


@mark.smoke
@mark.folder_structure
@mark.project_folder_structure
class ProjectFolderTests:

    # Test Data Paths
    TEST_DATA_INPUT = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataInput/"
    PROJECT_STRUCTURE_TEST_DATA = TEST_DATA_INPUT + "ProjectFolderStructure_test_input.yaml"

    @staticmethod
    def test_project_folder_structure(app_constants, load_test_input):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP34

        Check that the number of folders and files are correct in the project root
        """
        # count folders/files in project folder
        number_of_files = len(os.listdir(app_constants.PROJECT))

        # load expected project folder structure
        project_structure = load_test_input(ProjectFolderTests.PROJECT_STRUCTURE_TEST_DATA)
        # expected folders/files count in project folder
        expected_file_count = len(project_structure[0]["ProjectRootFolderStructure"])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_project_folder_content(app_constants, load_test_input):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP35

        Check that the all the folders and files are correct in the project root
        """
        # get the folder content
        files = os.listdir(app_constants.PROJECT)

        # load expected project folder structure
        project_structure = load_test_input(ProjectFolderTests.PROJECT_STRUCTURE_TEST_DATA)

        # compare folder content with the expected files
        assert all(file in files for file in project_structure[0]["ProjectRootFolderStructure"])
