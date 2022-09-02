from .. import constants
from pytest import mark
import re
import json


@mark.smoke
@mark.vb
@mark.user_guide
class UserGuideVBTests:

    def test_user_guide_version_as_expected_vb(self, read_pdf, test_data):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in UserGuide_test_data.yaml
        """
        user_guide = read_pdf(constants.VB_USER_GUIDE)

        # Extract text and do the search
        found = False
        for i in range(0, len(user_guide.pages)):
            page_obj = user_guide.pages[i]
            text = page_obj.extract_text()
            if re.search(test_data["release_version"], text):
                found = True

        if test_data["expected_result"] == "pass":
            assert found is True
        else:
            assert found is False


@mark.smoke
@mark.csharp
@mark.user_guide
class UserGuideCsharpTests:
    def test_user_guide_version_as_expected_csharp(self, read_pdf, test_data):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in UserGuide_test_data.yaml
        """
        user_guide = read_pdf(constants.CSHARP_USER_GUIDE)

        # Number of pages
        num_pages = len(user_guide.pages)

        # Extract text and do the search
        found = False
        for i in range(0, num_pages):
            PageObj = user_guide.pages[i]
            Text = PageObj.extract_text()
            if re.search(test_data["release_version"], Text):
                found = True

        if test_data["expected_result"] == "pass":
            assert found == True
        else:
            assert found == False
