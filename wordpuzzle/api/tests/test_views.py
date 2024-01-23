from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from api.models import WordPuzzle


class WordPuzzleApiTestCase(TestCase):
    def test_word_puzzle_api(self):
        # Define the input parameters
        start_word = "oyster"
        end_word = "mussel"

        # Build the URL using reverse
        url = reverse("wordpuzzle")

        # Make a GET request to the API endpoint
        response = self.client.get(url, {"startWord": start_word, "endWord": end_word})

        # Check that the response has a 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the structure of the JSON response
        expected_response = {
            "data": ["oyster", "ouster", "muster", "musted", "mussed", "mussel"]
        }

        response_data = response.json()

        self.assertEqual(response_data, expected_response)

    def test_word_puzzle_api_with_bad_request(self):
        url = reverse("wordpuzzle")

        # Send GET request with missing parameters
        response = self.client.get(url)

        # Assert the 400 response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
