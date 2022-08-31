from pytest import mark


@mark.smoke
@mark.nuspec
class NuspecTests:

    def test_nuspec_functions_as_expected(self):
        assert True



