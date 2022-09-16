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
        print(".variations" in data["designOptions"]["fileInfoCollection"])
        for element in data["designOptions"]["fileInfoCollection"]:
            if test_data_project_json["key"] in element:
                # Key was found and it shouldn't be present
                assert False

        # Key was not found and the test is successful
        assert True
