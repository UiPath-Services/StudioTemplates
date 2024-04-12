from pytest import mark


@mark.smoke
@mark.template_json
class TemplateJsonTests:
    @staticmethod
    def test_template_json_dependencies(convert_to_lower, load_json, app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP39

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
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP40

        Check if the main file is Main-ActionCenter
        """

        data = load_json(app_constants.TEMPLATE_JSON)

        assert app_constants.MAIN_ACTION_CENTER in data["MainFile"]

    @staticmethod
    def test_template_json_file_info_collection(convert_to_lower, load_json, app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP56

        Check if the FileInfoCollection field, which holds all the configured RPA tests,
        between project.json and template.json is the same.
        """
        vb_project_json = load_json(app_constants.PROJECT_JSON)
        vb_template_json = load_json(app_constants.TEMPLATE_JSON)

        vb_project_json = convert_to_lower(vb_project_json)
        vb_template_json = convert_to_lower(vb_template_json)
        vb_project_json_design_options = convert_to_lower(vb_project_json["designoptions"])

        assert vb_project_json_design_options["fileinfocollection"] == vb_template_json["fileinfocollection"]