from pytest import mark
import pandas as pd


@mark.smoke
@mark.config
class ConfigTests:

    @staticmethod
    def test_config_functions_as_expected(compare_config, app_constants):
        project_config = pd.read_excel(app_constants.PROJECT_CONFIG_FILE, sheet_name=None)
        expected_config = pd.read_excel(app_constants.EXPECTED_CONFIG_FILE, sheet_name=None)

        assert compare_config(project_config, expected_config)

