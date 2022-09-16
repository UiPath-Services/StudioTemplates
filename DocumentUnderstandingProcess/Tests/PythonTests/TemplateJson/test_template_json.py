from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:
    @staticmethod
    def test_project_template_json_dependencies(dependency_check, app_constants):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(app_constants.PROJECT_JSON, app_constants.TEMPLATE_JSON)
        assert result
