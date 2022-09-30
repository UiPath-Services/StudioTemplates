from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:
    @staticmethod
    def test_template_json_dependencies(convert_to_lower, load_json, app_constants):
        """
        Check if the dependencies field between project.json and template.json is the same
        """
        vb_project_json = load_json(app_constants.PROJECT_JSON)
        vb_template_json = load_json(app_constants.TEMPLATE_JSON)

        vb_project_json = convert_to_lower(vb_project_json)
        vb_template_json = convert_to_lower(vb_template_json)

        assert vb_project_json["dependencies"] == vb_template_json["dependencies"]

    @staticmethod
    def test_template_json_main_file(load_json, app_constants):
        """
        Check if the main file is Main-ActionCenter
        """

        data = load_json(app_constants.TEMPLATE_JSON)

        assert app_constants.MAIN_ACTION_CENTER in data["MainFile"]
