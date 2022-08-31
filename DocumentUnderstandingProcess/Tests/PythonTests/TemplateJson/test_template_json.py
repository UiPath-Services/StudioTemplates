from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:

    @mark.vb
    def test_template_json_dependencies_vb(self, dependency_check):
        dependency_check("asd.json", "project.json")
        assert True

    @mark.csharp
    def test_template_json_dependencies_csharp(self, dependency_check):
        dependency_check("asd.json", "project.json")
        assert True
