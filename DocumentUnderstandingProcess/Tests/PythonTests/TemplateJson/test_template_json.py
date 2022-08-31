from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:

    @mark.vb
    def test_project_template_json_dependencies_vb(self, dependency_check):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(
            "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/project.json",
            "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/.local/template.json")
        assert result

    @mark.csharp
    def test_project_template_json_dependencies_csharp(self, dependency_check):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        result = dependency_check(
            "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/CSharp/project.json",
            "../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/.local/template.json")
        assert result
