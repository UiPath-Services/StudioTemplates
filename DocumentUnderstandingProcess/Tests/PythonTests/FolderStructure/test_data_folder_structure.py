from pytest import mark
from .. import constants


@mark.vb
@mark.smoke
@mark.folder_structure
class DataFolderVBTests:

    def test_data_folder_structure_vb(self, count_files, comp_file_count):
        """
        Check the structure of the Data folder.
        """
        # count folders/files in Data folder

        num_files = count_files(constants.VB_DATA_FOLDER)

        # expected folders/files count in Data folder
        expected_file_count = 4

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_data_folder_content_vb(self, get_files, comp_files):
        """
        Check the content of the Data folder.
        """
        # get the folder content
        files = get_files(constants.VB_DATA_FOLDER)

        expected_files = ['Config.xlsx', 'ExampleDocuments', 'Exports', 'TempFolder']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_example_documents_folder_structure_vb(self, count_files, comp_file_count):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.VB_DATA_EXAMPLE_DOCS)

        # expected folders/files count in ExampleDocuments folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_exampled_ocuments_folder_content_vb(self, get_files, comp_files):
        """
        Check the content of the ExampleDocuments folder.
        """
        # get the folder content
        files = get_files(constants.VB_DATA_EXAMPLE_DOCS)

        expected_files = ['MergedDocuments.pdf']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_exports_folder_structure_vb(self, count_files, comp_file_count):
        """
        Check the content and structure of the Exports folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.VB_DATA_EXPORTS)

        # expected folders/files count in Exports folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_exports_folder_content_vb(self, get_files, comp_files):
        """
        Check the content of the Exports folder.
        """
        # get the folder content
        files = get_files(constants.VB_DATA_EXPORTS)

        expected_files = ['placeholder.txt']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_tempfolder_folder_structure_vb(self, count_files, comp_file_count):
        """
        Check the content and structure of the TempFolder folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.VB_DATA_TEMP_FOLDER)

        # expected folders/files count in TempFolder folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_tempfolder_folder_content_vb(self, get_files, comp_files):
        """
        Check the content of the TempFolder folder.
        """
        # get the folder content
        files = get_files(constants.VB_DATA_TEMP_FOLDER)

        expected_files = ['placeholder.txt']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)


@mark.csharp
@mark.smoke
@mark.folder_structure
class DataFolderCsharpTests:

    def test_data_folder_structure_csharp(self, count_files, comp_file_count):
        """
        Check the structure of the Data folder.
        """
        # count folders/files in Data folder
        num_files = count_files(constants.CSHARP_DATA_FOLDER)

        # expected folders/files count in Data folder
        expected_file_count = 4

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_data_folder_content_csharp(self, get_files, comp_files):
        """
        Check the content of the Data folder.
        """
        # get the folder content
        files = get_files(constants.CSHARP_DATA_FOLDER)

        expected_files = ['Config.xlsx', 'ExampleDocuments', 'Exports', 'TempFolder']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_exampledocuments_folder_structure_csharp(self, count_files, comp_file_count):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.CSHARP_DATA_EXAMPLE_DOCS)

        # expected folders/files count in ExampleDocuments folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_exampledocuments_folder_content_csharp(self, get_files, comp_files):
        """
        Check the content of the ExampleDocuments folder.
        """
        # get the folder content
        files = get_files(constants.CSHARP_DATA_EXAMPLE_DOCS)

        expected_files = ['MergedDocuments.pdf']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_exports_folder_structure_csharp(self, count_files, comp_file_count):
        """
        Check the content and structure of the Exports folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.CSHARP_DATA_EXPORTS)

        # expected folders/files count in Exports folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_exports_folder_content_csharp(self, get_files, comp_files):
        """
        Check the content of the Exports folder.
        """
        # get the folder content
        files = get_files(constants.CSHARP_DATA_EXPORTS)

        expected_files = ['placeholder.txt']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)

    def test_tempfolder_folder_structure_csharp(self, count_files, comp_file_count):
        """
        Check the content and structure of the TempFolder folder.
        """
        # count folders/files in the ExampleDocuments folder
        num_files = count_files(constants.CSHARP_DATA_TEMP_FOLDER)

        # expected folders/files count in TempFolder folder
        expected_file_count = 1

        # compare number of files with expected number of files
        assert comp_file_count(num_files, expected_file_count)

    def test_tempfolder_folder_content_csharp(self, get_files, comp_files):
        """
        Check the content of the TempFolder folder.
        """
        # get the folder content
        files = get_files(constants.CSHARP_DATA_TEMP_FOLDER)

        expected_files = ['placeholder.txt']

        # compare folder content with the expected files
        assert comp_files(files, expected_files)
