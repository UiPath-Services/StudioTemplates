from pytest import mark
import re

@mark.smoke
@mark.retry_scope
class ConfigTests:
    @staticmethod
    def test_configurable_retry_interval_values(app_constants, get_absolute_filenames, retry_interval):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP71

        Check that each retry activity has configurable values for the RetryInterval property.
        """
        # Regex for retry scope (not variable)
        retry_scope_re = re.compile('((ui:RetryScope).*)')
        # Regex for retry interval
        retry_interval_re = re.compile('(?<=RetryInterval=\").*?(?=\")')
        # Regex for retry interval value
        retry_interval_value_re = re.compile('([0-9][0-9]:[0-9][0-9]:[0-9][0-9])')

        configurable_value = True

        # Iterate through each XAML in the project
        framework_files = get_absolute_filenames(app_constants.PROJECT)
        for framework_file in framework_files:
            # in each workflow, search for the retry scope and check value in the RetryInterval property
            configurable_value = configurable_value and retry_interval(framework_file, retry_scope_re,
                                                                       retry_interval_re, retry_interval_value_re)

        assert configurable_value

    @staticmethod
    def test_configurable_retry_values(app_constants, get_absolute_filenames, retry_interval):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP72

        Check that each retry activity has configurable values for the NumberOfRetries property.
        """
        # Regex for retry scope (not variable)
        retry_scope_re = re.compile('((ui:RetryScope).*)')
        # Regex for number of retries
        number_of_retries_re = re.compile('(?<=NumberOfRetries=\").*?(?=\")')
        # Regex for number of retries value
        number_of_retries_value_re = re.compile('([0-9])')

        configurable_value = True

        # Iterate through each XAML in rhe project
        framework_files = get_absolute_filenames(app_constants.PROJECT)
        for framework_file in framework_files:
            # in each workflow, search for the retry scope and check value in the RetryInterval property
            configurable_value = configurable_value and retry_interval(framework_file, retry_scope_re,
                                                           number_of_retries_re, number_of_retries_value_re)

        assert configurable_value
