from pytest import mark


@mark.smoke
@mark.config
class ConfigTests:

    def test_config_functions_as_expected(self):
        assert True

