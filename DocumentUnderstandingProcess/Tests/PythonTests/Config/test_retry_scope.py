from pytest import mark
import os
import re

@mark.smoke
@mark.retry_scope
class ConfigTests:
    @staticmethod
    def test_configurable_retry_interval_values(app_constants, get_absolute_filenames):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP71

        Check that each retry activity has configurable values for the RetryInterval property.
        """

        def retry_interval(filename):
            """
            :param filename: XAML filename in which we search for presence of retry scope activity and RetryInterval property
            :return: True - the file does not have a retry scope activity
                     True - the file has retry scope activity and the RetryInterval property is configurable
                     False - the file has retry scope activity, but the RetryInterval property is not configurable
            """
            retry_scope_re = re.compile('((ui:RetryScope).*)')
            retry_interval_re = re.compile('(?<=RetryInterval=\").*?(?=\")')
            retry_interval_value_re = re.compile('([0-9][0-9]:[0-9][0-9]:[0-9][0-9])')

            digit_found = False

            with open(filename, "r") as f:
                content = f.read()
                retry_scope_tags = retry_scope_re.findall(content)
                for tag in retry_scope_tags:
                    retry_interval_value = retry_interval_re.search(tag[0])
                    # Check for NoneType
                    if retry_interval_value is not None:
                        retry_interval_value = retry_interval_value.group(0)
                        # check if value is configurable or hard coded
                        if retry_interval_value_re.search(retry_interval_value) != None:
                            print("\nFile "+filename+" has a retry scope with property RetryInterval hard coded")
                            digit_found = True

            return not digit_found

        ''' HERE STARTS THE FUNCTION '''
        result_value = True

        # Iterate through each XAML in the project
        framework_files = get_absolute_filenames(app_constants.PROJECT)
        for framework_file in framework_files:
            result_value = result_value and retry_interval(framework_file)

        assert result_value

    @staticmethod
    def test_configurable_retry_values(app_constants, get_absolute_filenames):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP72

        Check that each retry activity has configurable values for the NumberOfRetries property.
        """

        def retry_interval(filename):
            """
            :param filename: XAML filename in which we search for presence of retry scope activity and NumberOfRetries property
            :return: True - the file does not have a retry scope activity
                     True - the file has retry scope activity and the NumberOfRetries property is configurable
                     False - the file has retry scope activity, but the NumberOfRetries property is not configurable
            """
            retry_scope_re = re.compile('((ui:RetryScope).*)')
            number_of_retries_re = re.compile('(?<=NumberOfRetries=\").*?(?=\")')
            number_of_retries_value_re = re.compile('([0-9])')

            digit_found = False

            with open(filename, "r") as f:
                content = f.read()
                retry_scope_tags = retry_scope_re.findall(content)
                for tag in retry_scope_tags:
                    retry_interval_value = number_of_retries_re.search(tag[0])
                    # Check for NoneType
                    if retry_interval_value is not None:
                        retry_interval_value = retry_interval_value.group(0)
                        # check if value is configurable or hard coded
                        if number_of_retries_value_re.search(retry_interval_value) != None:
                            print("\nFile " + filename + " has a retry scope with property NumberOfRetries hard coded")
                            digit_found = True

            return not digit_found

        ''' HERE STARTS THE FUNCTION '''
        result_value = True

        # Iterate through each XAML in rhe project
        framework_files = get_absolute_filenames(app_constants.PROJECT)
        for framework_file in framework_files:
            result_value = result_value and retry_interval(framework_file)

        assert result_value
