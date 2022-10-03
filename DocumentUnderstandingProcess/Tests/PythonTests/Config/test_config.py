from pytest import mark
import pandas as pd


@mark.smoke
@mark.config
class ConfigTests:

    @staticmethod
    def test_config_functions_as_expected(app_constants):
        project_config = pd.read_excel(app_constants.PROJECT_CONFIG_FILE, sheet_name=None)
        expected_config = pd.read_excel(app_constants.EXPECTED_CONFIG_FILE, sheet_name=None)

        # initialize compare_result with True
        compare_result = True
        for key in expected_config.keys():
            # check if the expected_config = project_config and do a logical "and" with the compare_result
            compare_result = compare_result and (expected_config[key].equals(project_config[key]))
        assert compare_result

