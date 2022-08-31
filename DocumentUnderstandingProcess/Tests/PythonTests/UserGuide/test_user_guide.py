from pytest import mark
import re

@mark.smoke
@mark.user_guide
class UserGuideTests:

    def test_user_guide_version_as_expected_vb(self, read_pdf, test_data):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in test_data.json
        """
        user_guide = read_pdf("../../../DocumentUnderstandingProcess/contentFiles/any/any/pt0/VisualBasic/UserGuide/Document Understanding Process - User Guide.pdf")

        # Number of pages
        num_pages = len(user_guide.pages)

        # Extract text and do the search
        found = False
        for i in range(0, num_pages):
            PageObj = user_guide.pages[i]
            Text = PageObj.extract_text()
            if re.search(test_data["release_version"], Text):
                found = True
                # print("Pattern Found on Page: " + str(i))

        if test_data["expected_result"] == "pass":
            assert found == True
        else:
            assert found == False

    def test_user_guide_version_as_expected_csharp(self, read_pdf, test_data):
        """
        Check the User_Guide.pdf file for the correct value of the release version.
        Test with multiple values, which are saved in test_data.json
        """
        user_guide = read_pdf("../../../DocumentUnderstandingProcess/contentFiles/any/any/pt1/CSharp/UserGuide/Document Understanding Process - User Guide.pdf")

        # Number of pages
        num_pages = len(user_guide.pages)

        # Extract text and do the search
        found = False
        for i in range(0, num_pages):
            PageObj = user_guide.pages[i]
            Text = PageObj.extract_text()
            if re.search(test_data["release_version"], Text):
                found = True
                # print("Pattern Found on Page: " + str(i))

        if test_data["expected_result"] == "pass":
            assert found == True
        else:
            assert found == False
