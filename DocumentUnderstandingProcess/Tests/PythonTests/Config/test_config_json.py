from pytest import mark
import json


@mark.smoke
@mark.config
@mark.cross_platform
class ConfigJsonTests:

    @staticmethod
    def test_config_json_sections(app_constants):
        """
        Check that the Cross-platform config file is valid JSON and has the sections the process reads.
        """
        with open(app_constants.PROJECT_CONFIG_FILE, "r", encoding="utf-8-sig") as config_file:
            config = json.load(config_file)
        assert {"Settings", "Constants", "Assets"} <= set(config.keys())
