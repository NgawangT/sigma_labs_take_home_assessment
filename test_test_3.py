import unittest
from test_3 import sum_current_time


class TestSumCurrentTime(unittest.TestCase):
    def test_valid_time_format(self):
        # Test valid time format HH:MM:SS
        self.assertEqual(sum_current_time("01:02:03"), 6)
        self.assertEqual(sum_current_time("12:34:56"), 102)
        self.assertEqual(sum_current_time("01:10:10"), 21)

    def test_invalid_time_format(self):
        # Check if ValueError is raised for invalid time formats.
        with self.assertRaises(ValueError):
            sum_current_time("12:34")  # Incomplete time format
        with self.assertRaises(ValueError):
            sum_current_time("01:02:03:04")  # Extra component
        with self.assertRaises(ValueError):
            sum_current_time("12-34-56")  # Invalid delimiter

    def test_non_numeric_time_components(self):
        # Check if ValueError is raised for non-numeric time components.
        with self.assertRaises(ValueError):
            sum_current_time("12:34:abc")
        with self.assertRaises(ValueError):
            sum_current_time("xyz:01:02")

    def test_negative_time_components(self):
        # Check if ValueError is raised for negative time components
        with self.assertRaises(ValueError):
            sum_current_time("-1:02:03")
        with self.assertRaises(ValueError):
            sum_current_time("01:-2:03")
        with self.assertRaises(ValueError):
            sum_current_time("01:02:-3")

    def test_mixed_valid_invalid_format(self):
        # Check if ValueError is raised for mixed valid and invalid formats
        with self.assertRaises(ValueError):
            sum_current_time("12:34:56:78")
        with self.assertRaises(ValueError):
            sum_current_time("01:02:abc:04")
        with self.assertRaises(ValueError):
            sum_current_time("-1:02:03:04")


if __name__ == "__main__":
    unittest.main()
