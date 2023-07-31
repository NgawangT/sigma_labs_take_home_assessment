"""
This module contains the function to add up the time in format.
"""
# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    try:
        hours, minutes, seconds = map(int, time_str.split(":"))
        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError("Time components cannot be negative.")
        return hours + minutes + seconds
    except ValueError as exc:
        # Re-raise the exception with a more informative error message
        raise ValueError("Invalid time format. Expected HH:MM:SS.") from exc
