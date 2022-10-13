
class Constants:

    def __init__(self, env):

        # Language Selection
        self.PROJECT = {
            "vb": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/",
            "csharp": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/CSharp/"
        }[env]

        self.TEMPLATE_JSON = {
            "vb": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/.local/template.json",
            "csharp": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/.local/template.json"
        }[env]

        # Project Constants
        self.PROJECT_JSON = self.PROJECT + "project.json"
        self.USER_GUIDE = self.PROJECT + "UserGuide/Document Understanding Process - User Guide.pdf"
        self.DATA_FOLDER = self.PROJECT + "Data/"
        self.DATA_EXAMPLE_DOCS = self.DATA_FOLDER + "ExampleDocuments"
        self.DATA_EXPORTS = self.DATA_FOLDER + "Exports"
        self.DATA_TEMP_FOLDER = self.DATA_FOLDER + "TempFolder"
        self.PROJECT_CONFIG_FILE = self.DATA_FOLDER + "Config.xlsx"
        self.EXPECTED_CONFIG_FILE = self.PROJECT + "Tests/Cache/Config_Expected.xlsx"
        self.NUSPEC = "../../DocumentUnderstandingProcess/UiPath.Template.DocumentUnderstandingProcess.nuspec"
        self.MAIN_ACTION_CENTER = "Main-ActionCenter.xaml"
        self.MAIN_ATTENDED = "Main-Attended.xaml"
        self.MOCK = self.PROJECT + "Mocks/"
        self.MOCK_CONFIG = self.PROJECT + "Mocks/mock_config.json"
        self.MOCK_REUSABLE_FOLDER = self.PROJECT + "Mocks/Framework/ReusableWorkflows"
        self.ROOT_TEST_DATA_INPUT = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataInput/"
        self.MOCK_FOLDER_STRUCTURE_TEST_DATA = self.ROOT_TEST_DATA_INPUT + "MockFolderStructure_test_input.yaml"
