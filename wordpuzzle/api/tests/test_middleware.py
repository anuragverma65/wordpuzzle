from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from api.middleware import WordPuzzleMiddleware
from django.http import JsonResponse
from django.conf import settings
from unittest.mock import patch
import unittest
import traceback


class WordPuzzleMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = WordPuzzleMiddleware({})

    def test_middleware_request_validation(self):
        # Build the URL using reverse
        url = reverse("wordpuzzle")

        # Test case where start_word and end_word are not provided
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Both startWord and endWord must be provided."},
        )

        # Test case where start_word and end_word are of different lengths
        response = self.client.get(url, {"startWord": "start", "endWord": "end"})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Both startWord and endWord must be of the same length."},
        )

        # Test case where start_word and end_word contain letters and/or numbers
        response = self.client.get(url, {"startWord": "123", "endWord": "end"})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Both startWord and endWord must be of type string."},
        )

    def test_process_exception(self):
        settings.DEBUG = False
        request = self.create_fake_request()
        exception = Exception("Test Exception")

        # Mock log_error method
        self.middleware.log_error = lambda request, exception: None

        response: JsonResponse = self.middleware.process_exception(request, exception)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)

    def test_process_exception_debug_enabled(self):
        settings.DEBUG = True
        request = self.create_fake_request()
        exception = Exception("Test Exception")

        response = self.middleware.process_exception(request, exception)

        # When DEBUG is enabled, the middleware should not handle the exception
        self.assertIsNone(response)

    @patch("logging.error")
    def test_log_error(self, mock_logging_error):
        request = self.create_fake_request()
        exception = Exception("Test Exception")

        self.middleware.log_error(request, exception)

        # Verify that logging.error was called with the expected error message
        expected_error_message = f"Error in {request.build_absolute_uri()}: {repr(exception)}\n{traceback.format_exc()}"
        mock_logging_error.assert_called_once_with(expected_error_message)

    def create_fake_request(self):
        # Create a fake request for testing purposes
        fake_request = unittest.mock.Mock()
        fake_request.build_absolute_uri.return_value = "example.com"
        return fake_request
