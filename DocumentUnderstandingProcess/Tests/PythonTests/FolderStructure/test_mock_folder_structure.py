from pytest import mark
import os


@mark.smoke
@mark.folder_structure
@mark.mock_folder_structure
class MockFolderTests:

    # Test Data Paths
    MOCK_FOLDER_STRUCTURE_TEST_DATA = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataInput/MockFolderStructure_test_input.yaml"

    @staticmethod
    def test_project_mock_reusable_folder_structure(app_constants, load_test_input):
        """
        Check that the number of folders and files are correct in the project root
        """
        # count folders/files in mock folder
        number_of_files = len(os.listdir(app_constants.MOCK_REUSABLE_FOLDER))

        # load expected mock folder structure
        mock_structure = load_test_input(MockFolderTests.MOCK_FOLDER_STRUCTURE_TEST_DATA)
        # expected folders/files count in mock folder
        expected_file_count = len(mock_structure[0]['MockReusableFolderStructure'])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_project_mock_reusable_folder_content(app_constants, load_test_input):
        """
        Check that the all the folders and files are correct in the mock/reusableworkflows folder
        """
        # get the folder content
        files = os.listdir(app_constants.MOCK_REUSABLE_FOLDER)

        # load expected mock folder structure
        mock_structure = load_test_input(MockFolderTests.MOCK_FOLDER_STRUCTURE_TEST_DATA)

        # compare folder content with the expected files
        assert all(file in files for file in mock_structure[0]['MockReusableFolderStructure'])

    @staticmethod
    def test_project_mock_config_check(app_constants, load_json, get_filenames):
        """
        Check that all the mocks from the Mocks folder are in the config file
        """
        # get the filenames in the MOCK/Framework directory
        filenames = get_filenames(app_constants.MOCK)

        # load the mock_config
        mock_config = load_json(app_constants.MOCK_CONFIG)

        # get all mock file names from the mocks config and put them in a string; mock file names are separated by '_'
        all_mocks = ''
        for mock in mock_config['mockedWorkflows']:
            # find index of last occurence of '\\'
            last_occurance = mock['mockFilePath'].rfind('\\')
            # trim to get only the name and extension of the file
            mock_name = mock['mockFilePath'][last_occurance+1:]
            all_mocks = all_mocks + '_' + mock_name

        # get all mock file names from the mocks folder and put them in a string; mock file names are separated by '_'
        all_files = ''
        for file in filenames:
            all_files = all_files + '_' + file

        assert all_mocks == all_files
