import yaml
from pytest import mark


@mark.smoke
@mark.project_json
class ProjectJsonTests:
    @staticmethod
    def test_project_json_variation_path(get_test_data_project_json, app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP37

        Checks if the there are mentions of the .variation folder in the project.json
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", "r")))
        # print(get_test_data.load_data(app_constants.PROJECT_JSON_TEST_DATA))
        #
        for element in data["designOptions"]["fileInfoCollection"]:
            # check for the Key presence
            assert not get_test_data_project_json["key"] in element
            # assert not get_test_data(app_constants.PROJECT_JSON_TEST_DATA)["key"] in element

    @staticmethod
    def test_project_json_main_file(app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP38

        Checks if the main file is Main-ActionCenter
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", "r")))

        assert app_constants.MAIN_ACTION_CENTER in data["main"]

    @staticmethod
    def test_project_json_starts_in_background(app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP43

        Checks if the "Starts in Background" property is disabled.
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", "r")))

        assert data["runtimeOptions"]["requiresUserInteraction"]

    @staticmethod
    def test_project_json_supports_persistance(app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP44

        Checks if the "Supports Persistence" property is enabled.
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", "r")))

        assert data["runtimeOptions"]["supportsPersistence"]