from pytest import mark
import os

@mark.smoke
@mark.folder_structure
class DataFolderTests:

    def test_data_folder_structure_vb(self, count_files):
        """
        Check the structure of the Data folder.
        """
        Data_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/Data"

        # count folders/files in Data folder
        num_files = count_files(Data_folder_path)

        if num_files != 4:
            assert False
        else:
            assert True

        print(len(os.listdir(Data_folder_path)))
        print(os.listdir(Data_folder_path))

        # print(len(os.listdir(ExampleDocuments_folder_path)))
        # print(os.listdir(ExampleDocuments_folder_path))
        #
        # # count folders/files in the Exports folder
        # print(len(os.listdir(Exports_folder_path)))
        # print(os.listdir(Exports_folder_path))
        #
        # # count folders/files in the TempFolder folder
        # print(len(os.listdir(TempFolder_folder_path)))
        # print(os.listdir(TempFolder_folder_path))

    def test_data_folder_content_vb(self, count_files, get_files):
        """
        Check the content of the Data folder.
        """
        Data_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/Data"

        # get the folder content
        files = get_files(Data_folder_path)

        print(files)

        expected_files = ['Config.xlsx', 'ExampleDocuments', 'Exports', 'TempFolder']
        length = len(expected_files)

        for file in range(length):
            if file >= len(files):
                assert False
            elif files[file] != expected_files[file]:
                assert False

        assert True

    def test_exampledocuments_folder_structure_vb(self,count_files):
        """
        Check the content and structure of the ExampleDocuments folder.
        """
        ExampleDocuments_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/Data/ExampleDocuments"

        # count folders/files in the ExampleDocuments folder
        num_files = count_files(ExampleDocuments_folder_path)

        if num_files != 1:
            assert False
        else:
            assert True

    def test_exports_folder_structure_vb(self, count_files):
        """
        Check the content and structure of the Exports folder.
        """
        Exports_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/Data/Exports"

        # count folders/files in the ExampleDocuments folder
        num_files = count_files(Exports_folder_path)

        if num_files != 1:
            assert False
        else:
            assert True

    def test_tempfolder_folder_structure_vb(self, count_files):
        """
        Check the content and structure of the TempFolder folder.
        """
        TempFolder_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/Data/TempFolder"

        # count folders/files in the ExampleDocuments folder
        num_files = count_files(TempFolder_folder_path)

        if num_files != 1:
            assert False
        else:
            assert True

    def test_data_folder_structure_csharp(self):
        """
        Check the content and structure of the Data folder.
        """

        Data_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/Csharp/Data"
        ExampleDocuments_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/Csharp/Data/ExampleDocuments"
        Exports_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/Csharp/Data/Exports"
        TempFolder_folder_path = "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/Csharp/Data/TempFolder"

        assert True
