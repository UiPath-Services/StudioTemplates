from pytest import mark
import re

@mark.smoke
@mark.arguments_direction
class ArgumentsDirectionTests:
    @staticmethod
    def test_arguments_direction(app_constants, get_absolute_filenames, extract_argument_direction):
        """
        alpha.uipath.com/dualphatests
        Test Manager project: Document Understanding Process
        Test Case: DUP45

        Check that all arguments have the correct direction set.
        """
        # Regex for argument (not variable)
        argument_re = re.compile('((x:Property).*)')
        # Regex for arguments name
        name_re = re.compile('(?<=Name=\")((in|out|io)_[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)')
        # Regex for arguments type
        type_value_re = re.compile('(?<=Type=\").*?(?=\")')

        # List of tuples (filename, argument, direction)
        extracted_data = []

        # Iterate through each XAML in the project
        framework_files = get_absolute_filenames(app_constants.PROJECT)
        # search in each xaml for arguments and their direction
        for framework_file in framework_files:
            # return a tuple for each (filename, argument, direction)
            # add returned value of extract_argument_direction(), to the end of the list
            # format (filename1, argument1, direction1), (filename1, argument2, direction2), (filename2,..)
            extracted_data.extend(extract_argument_direction(framework_file, argument_re, name_re, type_value_re))

        # check that the prefix of each argument is the same as its direction
        test_result = True
        # for each tuple in the tuple list
        for tup in extracted_data:
            # the direction is InArgument(x:String), OutArgument or InOutArgument; transform this into in, out, io
            # InArgument(x:String) -> InArgument
            direction = tup[2][:tup[2].index("(")]
            # InArgument -> in
            direction = direction[:direction.index('A')].lower()
            if direction == "inout":
                direction = "io"
            # compare the argument prefix with its direction
            if tup[1][:tup[1].index('_')] != direction:
                # if they are not equal, write comment
                test_result = False
                print(f"\nFile {tup[0]}")
                print(f"Expected: argument {tup[1]} has {tup[1][:tup[1].index('_')]} direction.")
                print(f"Workflow: argument {tup[1]} has {direction} direction.")

        assert test_result
