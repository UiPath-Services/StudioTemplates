import yaml
from pytest import mark

# TODO: Fix the yaml, use fixtures.

@mark.smoke
@mark.template_json
class TemplateJsonTests:
    @staticmethod
    def test_template_json_dependencies(dependency_check, app_constants):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(app_constants.PROJECT_JSON, app_constants.TEMPLATE_JSON)
        assert result

    @staticmethod
    def test_template_json_main_file(app_constants):
        """
        Check if the main file is Main-ActionCenter
        """

        data = yaml.safe_load((open(app_constants.TEMPLATE_JSON, 'r')))
        assert app_constants.MAIN_ACTION_CENTER in data["MainFile"]
