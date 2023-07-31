"""
This module reads from the (people.csv) which contains information 
on people's home postcodes, and the type of court they desire. 
It accesses the courts and tribunals finder API to 
find the 10 nearest courts to a given postcode, and then
displays the nearest court details for each person, including the name, 
type of court desired, home postcode, nearest court of the right type, 
the dx_number (if available) of the nearest court, 
and the distance to the nearest court of the right type.
"""
import os
import pandas as pd
import requests

# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type


def get_csv_dict(csv_file: str) -> list[dict]:
    """
    Read the CSV file and returns a list of dictionaries,
    where each dictionary contains the person's details.

    Args:
        CSV_FILE (str): The path to the CSV file.
    """
    try:
        data_frm = pd.read_csv(csv_file)
        data_dict = data_frm[
            ["person_name", "home_postcode", "looking_for_court_type"]
        ].to_dict(orient="records")
        return data_dict
    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file '{csv_file}' is empty.")
        return []


class APIError(Exception):
    """Custom exception class for API-related errors."""

    def __init__(self, message, code=None, response=None):
        super().__init__(message)
        self.code = code
        self.response = response


def find_nearest_court(courts: list[dict], court_type: str) -> dict:
    """
    Find and return the nearest court of the specified court type.

    Args:
        courts (list[dict]): A list of dictionaries representing courts.
        court_type (str): The type of court desired by the person.
    """
    for court in courts:
        if court_type in court["types"]:
            return court
    return {}


def get_nearest_court(postcode: str, court_type: str) -> dict:
    """
    Returns a dictionary containing the details of the nearest court.

    Args:
        postcode (str): The postcode for which to find the nearest court.
        court_type (str): The type of court desired by the person.
    """
    try:
        url = f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        courts = response.json()
        return find_nearest_court(courts, court_type)
    except requests.exceptions.RequestException as error:
        raise APIError(
            f"Failed to fetch data from the API for postcode {postcode}. " f"{error}"
        ) from error
    except ValueError as error:
        raise APIError(
            f"Invalid JSON data returned from the API for postcode {postcode}. "
            f"{error}"
        ) from error


def format_output(person: dict, nearest_court: dict) -> dict:
    """
    Returns a dictionary containing the formatted output.

    Args:
        person (dict): A dictionary representing a person's details.
        nearest_court (dict): A dictionary representing the details of the nearest court.
    """
    try:
        output = {
            "name": person.get("person_name", ""),
            "type_of_court_desired": person.get("looking_for_court_type", ""),
            "home_postcode": person.get("home_postcode", ""),
            "nearest_court": nearest_court.get("name", ""),
            "distance_to_nearest_court": nearest_court.get("distance", ""),
        }

        dx_number = nearest_court.get("dx_number", "")

        if dx_number:
            output["dx_number"] = dx_number

        return output
    except KeyError as error:
        print(
            f"Failed to format output for person {person['person_name']}. Missing key: {error}"
        )
        return {}


def process_people_data(people_dict: list[dict]) -> list[dict]:
    """
    Main function to process the CSV data and fetch nearest court details for each person.

    Args:
        csv_file (str): The path to the CSV file containing person details.
    """
    result = []

    for person in people_dict:
        postcode = person["home_postcode"]
        court_type = person["looking_for_court_type"]

        try:
            nearest_court = get_nearest_court(postcode, court_type)
        except APIError as error:
            print(
                f"Error: Failed to get nearest court for {person['person_name']}. {error}"
            )
            continue  # Skip to the next person in case of error

        if nearest_court:
            person_output = format_output(person, nearest_court)
            result.append(person_output)

    return result


def csv_exists(csv_file: str) -> None:
    """Checks if file path exists."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file '{csv_file}' not found.")


def main():
    """main function to tie in the different functions together."""
    csv_file = "people.csv"
    csv_exists(csv_file)
    people_dict = get_csv_dict(csv_file)
    return process_people_data(people_dict)


if __name__ == "__main__":
    print(main())
