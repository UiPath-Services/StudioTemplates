from pytest import mark
import re


@mark.smoke
@mark.user_guide
class UserGuideTests:

    @staticmethod
    def test_user_guide_version_as_expected(read_pdf, test_data_user_guide, app_constants):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in UserGuide_test_data.yaml
        """
        user_guide = read_pdf(app_constants.USER_GUIDE)
        number_of_pages = len(user_guide.pages)
        output = ""

        # Extract text
        for i in range(0, number_of_pages):
            page_obj = user_guide.pages[i]
            output += page_obj.extract_text()

        # check for the presence of the release version in the user guide
        found = (re.search(test_data_user_guide["release_version"], output) is not None)
        should_pass = test_data_user_guide["expected_result"] == "pass"

        # asserting the presence of the release version in the user guide, considering also the expected_result
        assert should_pass == found
