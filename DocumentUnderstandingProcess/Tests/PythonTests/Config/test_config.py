from pytest import mark
import pandas as pd


@mark.smoke
@mark.config
class ConfigTests:
    @staticmethod
    def test_config_functions_as_expected(app_constants):
        project_config = pd.read_excel(app_constants.PROJECT_CONFIG_FILE, sheet_name=None)
        expected_config = pd.read_excel(app_constants.EXPECTED_CONFIG_FILE, sheet_name=None)

        for key in expected_config.keys():
            # check if the expected_config = project_config
            assert expected_config[key].equals(project_config[key])
