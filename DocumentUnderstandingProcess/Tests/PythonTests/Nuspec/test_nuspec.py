from pytest import mark


@mark.smoke
@mark.nuspec
class NuspecTests:
    @staticmethod
    def test_nuspec_version_as_expected(read_xml, test_data, app_constants):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP36

        Check the *.nuspec file for the correct value in the version field.
        Test with multiple values, which are saved in Nuspec_test_data.yaml
        """
        nuspec_xml = read_xml(app_constants.NUSPEC)
        should_pass = test_data["expected_result"] == "pass"
        # If the position of the tag version changes, this will fail. It is expected to have it as the 2nd item
        correct_version = test_data["release_version"] == nuspec_xml[0][1].text

        assert should_pass == correct_version
