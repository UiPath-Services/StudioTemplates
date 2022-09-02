from pytest import mark
from .. import constants
import os
import yaml

expected_results = yaml.safe_load((open('PythonTests/FolderStructure/expected_data.yaml', 'r')))


@mark.vb
@mark.smoke
@mark.folder_structure
class DataFolderVBTests:
    # todo: Resolve the code duplication. Only differences are the constants being sent.

    def test_data_folder_structure_vb(self):
        """
        Check the structure of the Data folder.
        """
        # count folders/files in Data folder
        num_files = len(os.listdir(constants.VB_DATA_FOLDER))

        # expected folders/files count in Data folder
        expected_file_count = expected_results['DataFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_data_folder_content_vb(self):
        """
        Check the content of the Data folder.
        """
        # get the folder content
        files = os.listdir(constants.VB_DATA_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['DataFolderFiles'])

    def test_example_documents_folder_structure_vb(self):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = len(os.listdir(constants.VB_DATA_EXAMPLE_DOCS))

        # expected folders/files count in ExampleDocuments folder
        expected_file_count = expected_results['ExampleDocumentsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_example_documents_folder_content_vb(self):
        """
        Check the content of the ExampleDocuments folder.
        """
        # get the folder content
        files = os.listdir(constants.VB_DATA_EXAMPLE_DOCS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExampleDocumentsFolderFiles'])

    def test_exports_folder_structure_vb(self):
        """
        Check the content and structure of the Exports folder.
        """
        # count folders/files in the Exports folder
        num_files = len(os.listdir(constants.VB_DATA_EXPORTS))

        # expected folders/files count in Exports folder
        expected_file_count = expected_results['ExportsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_exports_folder_content_vb(self):
        """
        Check the content of the Exports folder.
        """
        # get the folder content
        files = os.listdir(constants.VB_DATA_EXPORTS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExportsFolderFiles'])

    def test_tempfolder_folder_structure_vb(self):
        """
        Check the content and structure of the TempFolder folder.
        """
        # count folders/files in the TempFolder folder
        num_files = len(os.listdir(constants.VB_DATA_TEMP_FOLDER))

        # expected folders/files count in TempFolder folder
        expected_file_count = expected_results['TempfolderFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_tempfolder_folder_content_vb(self):
        """
        Check the content of the TempFolder folder.
        """
        # get the folder content
        files = os.listdir(constants.VB_DATA_TEMP_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['TempfolderFolderFiles'])


@mark.csharp
@mark.smoke
@mark.folder_structure
class DataFolderCsharpTests:

    def test_data_folder_structure_csharp(self):
        """
        Check the structure of the Data folder.
        """
        # count folders/files in Data folder
        num_files = len(os.listdir(constants.CSHARP_DATA_FOLDER))

        # expected folders/files count in Data folder
        expected_file_count = expected_results['DataFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_data_folder_content_csharp(self):
        """
        Check the content of the Data folder.
        """
        # get the folder content
        files = os.listdir(constants.CSHARP_DATA_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['DataFolderFiles'])

    def test_example_documents_folder_structure_csharp(self):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = len(os.listdir(constants.CSHARP_DATA_EXAMPLE_DOCS))

        # expected folders/files count in ExampleDocuments folder
        expected_file_count = expected_results['ExampleDocumentsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_example_documents_folder_content_csharp(self):
        """
        Check the content of the ExampleDocuments folder.
        """
        # get the folder content
        files = os.listdir(constants.CSHARP_DATA_EXAMPLE_DOCS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExampleDocumentsFolderFiles'])

    def test_exports_folder_structure_csharp(self):
        """
        Check the content and structure of the Exports folder.
        """
        # count folders/files in the Exports folder
        num_files = len(os.listdir(constants.CSHARP_DATA_EXPORTS))

        # expected folders/files count in Exports folder
        expected_file_count = expected_results['ExportsFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_exports_folder_content_csharp(self):
        """
        Check the content of the Exports folder.
        """
        # get the folder content
        files = os.listdir(constants.CSHARP_DATA_EXPORTS)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['ExportsFolderFiles'])

    def test_tempfolder_folder_structure_csharp(self):
        """
        Check the content and structure of the TempFolder folder.
        """
        # count folders/files in the TempFolder folder
        num_files = len(os.listdir(constants.CSHARP_DATA_TEMP_FOLDER))

        # expected folders/files count in TempFolder folder
        expected_file_count = expected_results['TempfolderFolderFileCount'][0]

        # compare number of files with expected number of files
        assert True if num_files == expected_file_count else False

    def test_tempfolder_folder_content_csharp(self):
        """
        Check the content of the TempFolder folder.
        """
        # get the folder content
        files = os.listdir(constants.CSHARP_DATA_TEMP_FOLDER)

        # compare folder content with the expected files
        assert all(file in files for file in expected_results['TempfolderFolderFiles'])
