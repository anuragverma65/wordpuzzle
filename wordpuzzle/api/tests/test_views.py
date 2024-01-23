from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from api.models import WordPuzzle
from unittest.mock import patch


class WordPuzzleApiTestCase(TestCase):
    def test_word_puzzle_api(self):
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

    def test_word_puzzle_api_uppercase(self):
        start_word = "HAS"
        end_word = "SUN"

        # Build the URL using reverse
        url = reverse("wordpuzzle")

        # Make a GET request to the API endpoint
        response = self.client.get(url, {"startWord": start_word, "endWord": end_word})

        # Check that the response has a 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the structure of the JSON response
        expected_response = {"data": ["has", "han", "san", "sun"]}

        response_data = response.json()

        self.assertEqual(response_data, expected_response)

    @patch("logging.info")
    def test_get_saved_result(self, mock_logging_info):
        # Create a WordPuzzle object with a saved result
        start_word = "bad"
        end_word = "dad"
        WordPuzzle.objects.create(
            start_word=start_word, end_word=end_word, sequence="bad,dad"
        )

        url = reverse("wordpuzzle")

        # Make a GET request to the view
        response = self.client.get(url, {"startWord": start_word, "endWord": end_word})

        expected_info_message = "Saved results found"

        mock_logging_info.assert_called_with(expected_info_message)

        # Check that the response contains the saved sequence
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"data": ["bad", "dad"]})

    def test_word_puzzle_api_with_bad_request(self):
        url = reverse("wordpuzzle")

        # Send GET request with missing parameters
        response = self.client.get(url)

        # Assert the 400 response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
