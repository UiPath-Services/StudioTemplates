from pytest import mark
from .. import constants


@mark.vb
@mark.smoke
@mark.template_json
class TemplateJsonVBTests:

    def test_project_template_json_dependencies_vb(self, dependency_check):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(constants.VB_PROJECT_JSON, constants.VB_TEMPLATE_JSON)
        assert result


@mark.csharp
@mark.smoke
@mark.template_json
class TemplateJsonCsharpTests:

    def test_project_template_json_dependencies_csharp(self, dependency_check):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(constants.CSHARP_PROJECT_JSON, constants.CSHARP_TEMPLATE_JSON)
        assert result
