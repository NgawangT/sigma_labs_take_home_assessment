"""
This module contains code to check a valid log line and return it.
Then return it as a dictionary. As well as contains tests for these
functions.
"""
from datetime import datetime

# [TODO]: step 1
# Update the is_log_line function below to skip lines that are not valid log lines.
# Valid log lines have a timestamp, error type, and message. For example, lines 1, 3,
# 7 and 37 are all examples of lines (from sample.log) that would be filtered out.
# There's no perfect way to do this: just decide what you think is reasonable to get
# the test to pass. The only thing you are not allowed to do is filter out log lines
# based on the exact row numbers you want to remove.


def is_valid_timestamp(timestamp: str) -> bool:
    """
    Returns True if valid timestamp. Else it return False.
    """
    date_format = "%m/%d/%y %H:%M:%S"

    try:
        # Attempt to parse the timestamp using the specified format
        datetime.strptime(timestamp, date_format)
        return True
    except ValueError:
        # If the timestamp doesn't match the format, it's invalid
        return False


def is_log_line(line:str) -> str:
    """Takes a log line and returns it if it is a valid log line and returns nothing
    if it is not.
    """
    if is_valid_timestamp(line[:17]):
        if line[17:26]:
            if line[26] == ":" and line[26:]:
                return line
    return None


# [TODO]: step 2
# Update the get_dict function below so it converts a line of the logs into a
# dictionary with keys for "timestamp", "log_level", and "message". The valid log
# levels are `INFO`, `TRACE`, and `WARNING`.
# See lines 67 to 71 (check test_step_2 expected) for how we expect the
# results to look.
def get_dict(line: str) -> dict:
    """Takes a log line and returns a dict with
    `timestamp`, `log_level`, `message` keys
    """
    valid_dict = {}

    valid_log = is_log_line(line)
    if valid_log:
        valid_dict["timestamp"] = line[:17]
    error = valid_log[17:26]
    if error != " ":
        valid_dict["log_level"] = error.strip()
    message = valid_log[26:]
    if message:
        valid_dict["message"] = message.strip()
    return valid_dict


# YOU DON'T NEED TO CHANGE ANYTHING BELOW THIS LINE
if __name__ == "__main__":

    def log_parser_step_1(log_file):
        """these are basic generators that will return
        1 line of the log file at a time"""
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield line

    def log_parser_step_2(log_file):
        """these are basic generators that will return
        1 line of the log file at a time"""
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield get_dict(line)

    # ---- OUTPUT --- #
    # You can print out each line of the log file line by line
    # by uncommenting this code below
    # for i, line in enumerate(log_parser("sample.log")):
    #     print(i, line)

    # ---- TESTS ---- #
    # DO NOT CHANGE

    def test_step_1():
        """Test for step 1"""
        with open("tests/step1.log") as f:
            test_lines = f.readlines()
        actual_out = list(log_parser_step_1("sample.log"))

        if actual_out == test_lines:
            print("STEP 1 SUCCESS")
        else:
            print(
                "STEP 1 FAILURE: step 1 produced unexpecting lines.\n"
                "Writing to failure.log if you want to compare it to tests/step1.log"
            )
            with open("step-1-failure-output.log", "w") as f:
                f.writelines(actual_out)

    def test_step_2():
        """Test for step 2"""
        expected = {
            "timestamp": "03/11/21 08:51:01",
            "log_level": "INFO",
            "message": ":.main: *************** RSVP Agent started ***************",
        }
        actual = next(log_parser_step_2("sample.log"))

        if expected == actual:
            print("STEP 2 SUCCESS")
        else:
            print(
                "STEP 2 FAILURE: your first item from the generator was not as expected.\n"
                "Printing both expected and your output:\n"
            )
            print(f"Expected: {expected}")
            print(f"Generator Output: {actual}")

    try:
        test_step_1()
    except Exception:
        print("step 1 test unable to run")

    try:
        test_step_2()
    except Exception:
        print("step 2 test unable to run")
