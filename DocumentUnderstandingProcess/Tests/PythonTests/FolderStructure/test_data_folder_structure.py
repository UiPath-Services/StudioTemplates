from pytest import mark
import os


@mark.smoke
@mark.folder_structure
class FolderTests:

    @staticmethod
    def test_data_folder_structure(app_constants, test_data_folder):
        """
        Check the structure of the Data folder and its inner folders.
        """
        # count folders/files in Data folder
        number_of_files = len(os.listdir(app_constants.PROJECT + test_data_folder['folderPath']))

        # expected folders/files count in Data folder
        expected_file_count = len(test_data_folder['FolderStructure'])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_data_folder_content(app_constants, test_data_folder):
        """
        Check the content of the Data folder and its inner folders.
        """
        # get the folder content
        files = os.listdir(app_constants.PROJECT + test_data_folder['folderPath'])

        # compare folder content with the expected files
        assert all(file in files for file in test_data_folder['FolderStructure'])

    @staticmethod
    def test_project_folder_structure(app_constants, test_project_folder):
        """
        Check that the number of folders and files are correct in the project root
        """
        # count folders/files in Data folder
        number_of_files = len(os.listdir(app_constants.PROJECT))

        # expected folders/files count in Data folder
        expected_file_count = len(test_project_folder['ProjectRootFolderStructure'])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_project_folder_content(app_constants, test_project_folder):
        """
        Check that the all the folders and files are correct in the project root
        """
        # get the folder content
        files = os.listdir(app_constants.PROJECT)

        # compare folder content with the expected files
        assert all(file in files for file in test_project_folder['ProjectRootFolderStructure'])

    @staticmethod
    def test_project_mock_reusable_folder_structure(app_constants, test_mock_folder):
        """
        Check that the number of folders and files are correct in the project root
        """
        # count folders/files in Data folder
        number_of_files = len(os.listdir(app_constants.MOCK_REUSABLE_FOLDER))

        # expected folders/files count in Data folder
        expected_file_count = len(test_mock_folder['MockReusableFolderStructure'])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_project_mock_reusable_folder_content(app_constants, test_mock_folder):
        """
        Check that the all the folders and files are correct in the mock/reusableworkflows folder
        """
        # get the folder content
        files = os.listdir(app_constants.MOCK_REUSABLE_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in test_mock_folder['MockReusableFolderStructure'])

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
