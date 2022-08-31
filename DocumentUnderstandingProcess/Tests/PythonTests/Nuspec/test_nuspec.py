from pytest import mark


@mark.smoke
@mark.nuspec
class NuspecTests:

    def test_nuspec_version_as_expected(self, read_xml, test_data):
        """
        Check the *.nuspec file for the correct value in the version field.
        Test with multiple values, which are saved in test_data.json
        """
        nuspec_xml = read_xml("../../../DocumentUnderstandingProcess/UiPath.Template.DocumentUnderstandingProcess.nuspec")

        # for each element in the xml
        for element in nuspec_xml[0]:
            # search for tag <version>
            if element.tag.find('version') != -1:
                # if <version> tag is found, read its value
                release_version = element.text

        # asserting the text from tag <version> with the actual release version
        if test_data["expected_result"] == "pass":
            assert release_version == test_data["release_version"]
        else:
            assert release_version != test_data["release_version"]



