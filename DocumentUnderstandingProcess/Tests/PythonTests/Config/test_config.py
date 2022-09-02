from pytest import mark
from .. import constants
import pandas as pd


@mark.smoke
@mark.config
class ConfigVBTests:

    @staticmethod
    def test_config_functions_as_expected(compare_config):
        project_config = pd.read_excel(constants.VB_PROJECT_CONFIG_FILE, sheet_name=None)
        expected_config = pd.read_excel(constants.VB_EXPECTED_CONFIG_FILE, sheet_name=None)

        assert compare_config(project_config, expected_config)

@mark.smoke
@mark.config
class ConfigVCsharpTests:

    @staticmethod
    def test_config_functions_as_expected(compare_config):
        project_config = pd.read_excel(constants.CSHARP_PROJECT_CONFIG_FILE, sheet_name=None)
        expected_config = pd.read_excel(constants.CSHARP_EXPECTED_CONFIG_FILE, sheet_name=None)

        assert compare_config(project_config, expected_config)
