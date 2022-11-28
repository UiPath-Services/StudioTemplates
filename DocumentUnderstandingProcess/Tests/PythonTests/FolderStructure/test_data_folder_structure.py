from pytest import mark
import os


@mark.smoke
@mark.folder_structure
@mark.data_folder_structure
class DataFolderTests:
    @staticmethod
    def test_data_folder_structure(app_constants, test_data):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP29

        Check the structure of the Data folder and its inner folders.
        """
        # count folders/files in Data folder
        number_of_files = len(os.listdir(app_constants.PROJECT + test_data["folderPath"]))

        # expected folders/files count in Data folder
        expected_file_count = len(test_data["FolderStructure"])

        # compare number of files with expected number of files
        assert number_of_files == expected_file_count

    @staticmethod
    def test_data_folder_content(app_constants, test_data):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP30

        Check the content of the Data folder and its inner folders.
        """
        # get the folder content
        files = os.listdir(app_constants.PROJECT + test_data["folderPath"])

        # compare folder content with the expected files
        assert all(file in files for file in test_data["FolderStructure"])
