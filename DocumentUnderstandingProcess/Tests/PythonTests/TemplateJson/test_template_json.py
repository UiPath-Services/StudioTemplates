from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:

    @mark.parametrize("dependency_check",
             ["./../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/project.json",
              "../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/.local/template.json"]
             )
    def test_template_json_dependencies_vb(self, dependency_check):
        assert dependency_check()

    # @mark.csharp
    # def test_template_json_dependencies_csharp(self, dependency_check):
    #     dependency_check("../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/CSharp/project.json", "../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/.local/template.json")
    #     assert True
