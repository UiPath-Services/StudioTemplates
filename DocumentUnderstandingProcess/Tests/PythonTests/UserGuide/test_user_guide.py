from pytest import mark
import re


@mark.smoke
@mark.user_guide
class UserGuideTests:
    @staticmethod
    def test_user_guide_version_as_expected(
        read_pdf, get_test_data_user_guide, app_constants
    ):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in UserGuide_test_data.yaml
        """
        user_guide = read_pdf(app_constants.USER_GUIDE)

        # Extract text
        output = user_guide.pages[4].extract_text()
        output = output.split("\n")[-1].replace("  ", "|")

        # check for the presence of the release version in the user guide
        found = re.search(get_test_data_user_guide["release_version"], output) is not None
        should_pass = get_test_data_user_guide["expected_result"] == "pass"

        # asserting the presence of the release version in the user guide, considering also the expected_result
        assert should_pass == found
