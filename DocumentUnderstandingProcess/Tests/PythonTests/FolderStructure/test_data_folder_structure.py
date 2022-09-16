from pytest import mark
import os
import yaml

expected_results = yaml.safe_load((open('TestDataGeneration/PythonTests/FolderStructure_test_data.yaml', 'r')))


@mark.smoke
@mark.folder_structure
class DataFolderTests:

    @staticmethod
    def test_data_folder_structure(app_constants):
        """
        Check the structure of the Data folder.
        """
        # count folders/files in Data folder
        number_of_files = len(os.listdir(app_constants.DATA_FOLDER))

        # expected folders/files count in Data folder
        expected_file_count = expected_results['DataFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if number_of_files == expected_file_count else False

    @staticmethod
    def test_data_folder_content(app_constants):
        """
        Check the content of the Data folder.
        """
        # get the folder content
        files = os.listdir(app_constants.DATA_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['DataFolderFiles'])

    @staticmethod
    def test_example_documents_folder_structure(app_constants):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        # count folders/files in the ExampleDocuments folder
        number_of_files = len(os.listdir(app_constants.DATA_EXAMPLE_DOCS))

        # expected folders/files count in ExampleDocuments folder
        expected_file_count = expected_results['ExampleDocumentsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if number_of_files == expected_file_count else False

    @staticmethod
    def test_example_documents_folder_content(app_constants):
        """
        Check the content of the ExampleDocuments folder.
        """
        # get the folder content
        files = os.listdir(app_constants.DATA_EXAMPLE_DOCS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExampleDocumentsFolderFiles'])

    @staticmethod
    def test_exports_folder_structure(app_constants):
        """
        Check the content and structure of the Exports folder.
        """
        # count folders/files in the Exports folder
        number_of_files = len(os.listdir(app_constants.DATA_EXPORTS))

        # expected folders/files count in Exports folder
        expected_file_count = expected_results['ExportsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if number_of_files == expected_file_count else False

    @staticmethod
    def test_exports_folder_content(app_constants):
        """
        Check the content of the Exports folder.
        """
        # get the folder content
        files = os.listdir(app_constants.DATA_EXPORTS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExportsFolderFiles'])

    @staticmethod
    def test_tempfolder_folder_structure(app_constants):
        """
        Check the content and structure of the TempFolder folder.
        """
        # count folders/files in the TempFolder folder
        number_of_files = len(os.listdir(app_constants.DATA_TEMP_FOLDER))

        # expected folders/files count in TempFolder folder
        expected_file_count = expected_results['TempfolderFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if number_of_files == expected_file_count else False

    # TODO: Check with @teodora if this actually works as intended. Probably not
    @staticmethod
    def test_tempfolder_folder_content(app_constants):
        """
        Check the content of the TempFolder folder.
        """
        # get the folder content
        files = os.listdir(app_constants.DATA_TEMP_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['TempfolderFolderFiles'])

    @staticmethod
    def test_project_folder_structure(app_constants):
        """
        Check that the all the folders and files are correct in the project root
        """

        # get the root folder
        files = os.listdir(app_constants.PROJECT)
        for file in files:
            if file not in expected_results['ProjectRootFolderStructure']:

                # one of the folders/files is missing
                assert False

        # we found all folders/files
        assert True

