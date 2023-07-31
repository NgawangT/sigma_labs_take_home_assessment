import unittest
import requests
from unittest.mock import patch
from test_2 import (
    csv_exists,
    get_csv_dict,
    APIError,
    find_nearest_court,
    get_nearest_court,
    format_output,
    process_people_data,
    pd,
)


class TestCSVFunctions(unittest.TestCase):
    @patch("os.path.exists")
    def test_csv_exists_file_found(self, mock_exists):
        mock_exists.return_value = True
        csv_file = "people.csv"
        result = csv_exists(csv_file)

        # Assert that the function does not raise an error
        self.assertIsNone(result)

    @patch("os.path.exists")
    def test_csv_exists_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        csv_file = "invalid.csv"

        # Assert that the function raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            csv_exists(csv_file)

    @patch("pandas.read_csv")
    def test_get_csv_dict_empty_csv(self, mock_read_csv):
        # Configure the mock read_csv function to raise an EmptyDataError
        mock_read_csv.side_effect = pd.errors.EmptyDataError(
            "No columns to parse from file"
        )
        csv_file = "empty.csv"
        data_dict = get_csv_dict(csv_file)

        # Assert that the function returns an empty list
        self.assertEqual(data_dict, [])


class TestGetNearestCourt(unittest.TestCase):
    @patch("test_2.requests.get")
    def test_get_nearest_court(self, mock_requests_get):
        # Test input data
        postcode = "E144PU"
        court_type = "Tribunal"
        # Test API response data
        api_response_data = [
            {"name": "Some Other Court", "types": ["Other"], "distance": 0.5},
            {"name": "Fake Tribunal 1", "types": ["Tribunal"], "distance": 1.29},
            {"name": "Fake Tribunal 2", "types": ["Tribunal"], "distance": 2.30},
        ]
        # Configure the mock response for requests.get
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = api_response_data
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        result = get_nearest_court(postcode, court_type)

        # Assert the result
        expected_result = {
            "name": "Fake Tribunal 1",
            "types": ["Tribunal"],
            "distance": 1.29,
        }
        self.assertEqual(result, expected_result)
        # Assert that requests.get was called with the correct URL
        expected_url = f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}"
        mock_requests_get.assert_called_once_with(expected_url)

    @patch("test_2.requests.get")
    def test_get_nearest_court_api_error(self, mock_requests_get):
        # Test input data
        postcode = "E144PU"
        court_type = "Tribunal"
        # Configure the mock response for requests.get to raise an exception
        mock_requests_get.side_effect = requests.exceptions.RequestException(
            "Test error"
        )

        # Call the function with sample data
        with self.assertRaises(APIError):
            get_nearest_court(postcode, court_type)

        # Assert that requests.get was called with the correct URL
        expected_url = f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}"
        mock_requests_get.assert_called_once_with(expected_url)


class TestFindNearestCourt(unittest.TestCase):
    def test_find_nearest_court_found(self):
        courts = [
            {
                "types": ["Tribunal"],
                "name": "Court 1",
            },
            {
                "types": ["Other"],
                "name": "Court 2",
            },
            {
                "types": ["Tribunal"],
                "name": "Court 3",
            },
        ]
        court_type = "Tribunal"

        result = find_nearest_court(courts, court_type)

        expected_result = {"types": ["Tribunal"], "name": "Court 1"}
        self.assertEqual(result, expected_result)

    def test_find_nearest_court_not_found(self):
        courts = [
            {
                "types": ["Other"],
                "name": "Court 2",
            },
            {
                "types": ["Other"],
                "name": "Court 4",
            },
        ]
        court_type = "Tribunal"

        result = find_nearest_court(courts, court_type)

        # Assert the result is an empty dictionary since the court_type was not found
        self.assertEqual(result, {})

    def test_find_nearest_court_empty_list(self):
        courts = []
        court_type = "Tribunal"

        result = find_nearest_court(courts, court_type)

        # Assert the result is an empty dictionary since the list of courts is empty
        self.assertEqual(result, {})


class TestFormatOutput(unittest.TestCase):
    def test_format_output_with_dx_number(self):
        person = {
            "person_name": "John Doe",
            "looking_for_court_type": "Tribunal",
            "home_postcode": "12345",
        }
        nearest_court = {
            "name": "Court 1",
            "distance": 1.29,
            "dx_number": "141420 Bloomsbury 7",
        }

        result = format_output(person, nearest_court)

        expected_result = {
            "name": "John Doe",
            "type_of_court_desired": "Tribunal",
            "home_postcode": "12345",
            "nearest_court": "Court 1",
            "distance_to_nearest_court": 1.29,
            "dx_number": "141420 Bloomsbury 7",
        }
        self.assertEqual(result, expected_result)

    def test_format_output_without_dx_number(self):
        person = {
            "person_name": "Jane Smith",
            "looking_for_court_type": "Other",
            "home_postcode": "67890",
        }
        nearest_court = {"name": "Court 2", "distance": 2.55, "dx_number": None}

        result = format_output(person, nearest_court)

        expected_result = {
            "name": "Jane Smith",
            "type_of_court_desired": "Other",
            "home_postcode": "67890",
            "nearest_court": "Court 2",
            "distance_to_nearest_court": 2.55,
        }
        self.assertEqual(result, expected_result)


class TestProcessPeopleData(unittest.TestCase):
    @patch("test_2.get_nearest_court")
    def test_process_people_data_with_nearest_court(self, mock_get_nearest_court):
        people_dict = [
            {
                "person_name": "John Doe",
                "looking_for_court_type": "Tribunal",
                "home_postcode": "12345",
            },
            {
                "person_name": "Jane Smith",
                "looking_for_court_type": "Other",
                "home_postcode": "67890",
            },
        ]

        # Configure the mock get_nearest_court function to return nearest court details
        mock_get_nearest_court.side_effect = [
            {"name": "Court 1", "distance": 1.29, "dx_number": "141420 Bloomsbury 7"},
            {"name": "Court 2", "distance": 2.55, "dx_number": None},
        ]

        result = process_people_data(people_dict)

        expected_result = [
            {
                "name": "John Doe",
                "type_of_court_desired": "Tribunal",
                "home_postcode": "12345",
                "nearest_court": "Court 1",
                "distance_to_nearest_court": 1.29,
                "dx_number": "141420 Bloomsbury 7",
            },
            {
                "name": "Jane Smith",
                "type_of_court_desired": "Other",
                "home_postcode": "67890",
                "nearest_court": "Court 2",
                "distance_to_nearest_court": 2.55,
            },
        ]
        self.assertEqual(result, expected_result)

    @patch("test_2.get_nearest_court")
    def test_process_people_data_with_api_error(self, mock_get_nearest_court):
        people_dict = [
            {
                "person_name": "John Doe",
                "looking_for_court_type": "Tribunal",
                "home_postcode": "12345",
            },
            {
                "person_name": "Jane Smith",
                "looking_for_court_type": "Other",
                "home_postcode": "67890",
            },
        ]

        # Configure the mock get_nearest_court function to raise an APIError
        mock_get_nearest_court.side_effect = APIError("API Error")

        result = process_people_data(people_dict)

        # Assert the result is an empty list since there was an error
        self.assertEqual(result, [])
