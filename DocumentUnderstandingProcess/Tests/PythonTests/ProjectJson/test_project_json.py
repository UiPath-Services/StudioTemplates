import yaml
from pytest import mark


@mark.smoke
@mark.project_json
class ProjectJsonTests:
    @staticmethod
    def test_project_json_variation_path(test_data_project_json, app_constants):
        """
        Checks if the there are mentions of the .variation folder in the project.json
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", 'r')))

        # initialize found_result with True
        found_result = False
        for element in data["designOptions"]["fileInfoCollection"]:
            # check for the Key presence and do a logical "or" with the found_result
            found_result = found_result or (test_data_project_json["key"] in element)

        # if Key was found, the test is failed
        assert not found_result

    @staticmethod
    def test_project_json_main_file(app_constants):
        """
        Checks if the main file is Main-ActionCenter
        """
        data = yaml.safe_load((open(app_constants.PROJECT + "\\project.json", 'r')))

        assert app_constants.MAIN_ACTION_CENTER in data["main"]



