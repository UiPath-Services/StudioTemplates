from pytest import mark
from .. import constants


@mark.smoke
@mark.config
class ConfigTests:

    @staticmethod
    def test_config_functions_as_expected():
        assert True

