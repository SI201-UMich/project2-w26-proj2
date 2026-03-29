# SI 201 HW4 (Library Checkout System)
# Your name: Sophia Jun and Kayla Sirefman
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================

    # ==============================
    with open(html_path, "r", encoding = "utf-8-sig") as file:
        soup = BeautifulSoup(file, "html.parser")
        
        listing_results = []

        for title_tag in soup.find_all(attrs={"data-testid": "listing-card-title"}):
            title = title_tag.get_text(strip=True)
            listing_id = ""

            title_id = title_tag.get("id", "")
            id_match = re.search(r"title_(\d+)", title_id)
            if id_match:
                listing_id = id_match.group(1)

            if listing_id:
                listing_results.append((title, listing_id))

        return listing_results



    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_dir = os.path.abspath(os.path.dirname(__file__))
    html_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")

    with open(html_path, "r", encoding="utf-8-sig") as file:
        soup = BeautifulSoup(file, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    policy_match = re.search(r"Policy number:\s*([A-Za-z0-9\-]+)", page_text)
    policy_number = policy_match.group(1) if policy_match else ""    

    host_type = "Superhost" if "Superhost" in page_text else "Not Superhost"
    overview_heading = soup.find("h2", string=re.compile(r"hosted by", re.I))
    host_name = ""
    room_type = ""

    if overview_heading is not None:
        heading_text = overview_heading.get_text(" ", strip=True).replace("\xa0", " ")
        host_match = re.search(r"hosted by\s+(.+)$", heading_text, re.I)
        if host_match:
            host_name = host_match.group(1).strip()
        if heading_text.lower().startswith("entire"):
            room_type = "Entire Room"
        elif heading_text.lower().startswith("private room"):
            room_type = "Private Room"
    location_match = re.search(r"Location\s*([0-9]\.[0-9])", page_text)
    location_rating = float(location_match.group(1)) if location_match else 0.0
    return {listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating,
        }
    }       



    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_data = []
    listing_results = load_listing_results(html_path)

    for listing_title, listing_id in listing_results:
        details = get_listing_details(listing_id)[listing_id]
        listing_data.append(
            (
                listing_title,
                listing_id,
                details["policy_number"],
                details["host_type"],
                details["host_name"],
                details["room_type"],
                details["location_rating"],

            )
        )
    return listing_data


    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key = lambda row: row[6], reverse=True)

    with open(filename, "w", newline="", encoding = "utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "Listing Title",
            "Listing ID",
            "Policy Number",
            "Host Type",
            "Host Name",
            "Room Type",
            "Location Rating",
        ])
        writer.writerows(sorted_data)

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings_by_room_type = {}

    for row in data:
        room_type = row[5]
        location_rating = row[6]

        if location_rating == 0.0:
            continue
        if room_type not in ratings_by_room_type:
            ratings_by_room_type[room_type] = []
        ratings_by_room_type[room_type].append(location_rating)
    averages = {}
    for room_type, ratings in ratings_by_room_type.items():
        averages[room_type] = sum(ratings) / len(ratings)
    return averages 
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_listings = []
    valid_pattern = re.compile(r"^(STR-\d{7}|\d{4}-\d{6}STR)$", re.I)

    for row in data:
        listing_id = row[1]
        policy_number = row[2].strip()

        if policy_number.lower() in ["pending", "exempt"]:
            continue

        if not valid_pattern.match(policy_number):
            invalid_listings.append(listing_id)

    return invalid_listings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar"
    params = {"q": query}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            "AppleWebKit/537.36 (KHTML, Like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, params = params, headers = headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    titles = []

    for title_tag in soup.find_all("h3", class_="gs_rt"):
        title = title_tag.get_text(" ", strip=True)
        if title:
            titles.append(title)
    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        details_list = [get_listing_details(listing_id) for listing_id in html_list]
        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.

        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(details_list[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(details_list[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(details_list[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(details_list[2]["1944564"]["location_rating"], 4.9)



    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for listing in self.detailed_data:
            self.assertEqual(len(listing), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(
            self.detailed_data[-1],
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        )
           


    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        output_csv(self.detailed_data, out_path)

        with open(out_path, "r", encoding="utf-8-sig") as csv_file:
            rows = list(csv.reader(csv_file))
        self.assertEqual(
            rows[1],
            ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        )

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)
        self.assertEqual(avg_ratings["Private Room"], 4.9)


    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])



def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    search_results_path = os.path.join(base_dir, "html_files","search_results.html")
    detailed_data = create_listing_database(search_results_path)
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)