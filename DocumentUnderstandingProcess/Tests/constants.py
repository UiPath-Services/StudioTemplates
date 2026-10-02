class Constants:
    def __init__(self, env):

        # Language Selection
        self.PROJECT = {
            "VB": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/",
            "Cross-platform": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt3/VisualBasic/",
        }[env]

        self.TEMPLATE_JSON = {
            "VB": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/.local/template.json",
            "Cross-platform": "../../DocumentUnderstandingProcess/contentFiles/any/any/pt3/.local/template.json",
        }[env]

        # Variant Constants
        self.IS_CROSS_PLATFORM = env == "Cross-platform"
        self.REQUIRES_USER_INTERACTION = not self.IS_CROSS_PLATFORM

        # Project Constants
        self.PROJECT_JSON = self.PROJECT + "project.json"
        self.USER_GUIDE = self.PROJECT + "UserGuide/Document Understanding Process - User Guide.pdf"
        self.DATA_FOLDER = self.PROJECT + "Data/"
        self.DATA_EXAMPLE_DOCS = self.DATA_FOLDER + "ExampleDocuments"
        self.DATA_EXPORTS = self.DATA_FOLDER + "Exports"
        self.DATA_TEMP_FOLDER = self.DATA_FOLDER + "TempFolder"
        self.PROJECT_CONFIG_FILE = self.DATA_FOLDER + ("config.json" if self.IS_CROSS_PLATFORM else "Config.xlsx")
        self.EXPECTED_CONFIG_FILE = self.PROJECT + "Tests/Cache/Config_Expected.xlsx"
        self.NUSPEC = "../../DocumentUnderstandingProcess/UiPath.Template.DocumentUnderstandingProcess.nuspec"
        self.MAIN_ACTION_CENTER = "Main-ActionCenter.xaml"
        self.MAIN_ATTENDED = "Main-Attended.xaml"
        self.FRAMEWORK = self.PROJECT + "Framework"
        self.MOCK = self.PROJECT + "Mocks/"
        self.MOCK_CONFIG = self.PROJECT + "Mocks/mock_config.json"
        self.MOCK_REUSABLE_FOLDER = self.PROJECT + "Mocks/Framework/ReusableWorkflows"
        self.ROOT_TEST_DATA_INPUT = "../../DocumentUnderstandingProcess/Tests/TestDataGeneration/PythonTests/TestDataInput/"
        self.MOCK_FOLDER_STRUCTURE_TEST_DATA = self.ROOT_TEST_DATA_INPUT + "MockFolderStructure_test_input.yaml"
        self.STANDARD_ANNOTATIONS_TEST_DATA = self.ROOT_TEST_DATA_INPUT + "StandardAnnotations_test_input.yaml"
        self.ARGUMENTS_DIRECTION_TEST_DATA = self.ROOT_TEST_DATA_INPUT + "ArgumentsDirection_test_input.yaml"
        self.PROJECT_STRUCTURE_TEST_DATA = self.ROOT_TEST_DATA_INPUT + (
            "ProjectFolderStructure_CrossPlatform_test_input.yaml" if self.IS_CROSS_PLATFORM else "ProjectFolderStructure_test_input.yaml")