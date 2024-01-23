from django.http import JsonResponse
from django.conf import settings
import logging
import traceback


class WordPuzzleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # Django calls process_exception() when a view raises an exception
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                self.log_error(request, exception)
            return JsonResponse(
                {
                    "error": "Something went wrong while processing your request. Please try again."
                },
                status=500,
            )

    def __call__(self, request):
        logging.info(f"Incoming request: {request.path}")

        # Exclude Swagger URLs from the pre-processing check
        if request.path.startswith("/api/wordpuzzle"):
            # Validate request parameters
            validation_result = self.validate_request_parameters(request)
            if validation_result is not None:
                return validation_result

            # Continue with the request processing
            response = self.get_response(request)
            return response
        return self.get_response(request)

    def log_error(self, request, exception):
        # Format and log the error message
        error_message = f"Error in {request.build_absolute_uri()}: {repr(exception)}\n{traceback.format_exc()}"
        logging.error(error_message)

    def validate_request_parameters(self, request):
        # Check if startWord and endWord are provided.
        start_word = request.GET.get("startWord", "")
        end_word = request.GET.get("endWord", "")

        # Check if the request body contains both words
        if not start_word or not end_word:
            return JsonResponse(
                {"error": "Both startWord and endWord must be provided."},
                status=400,
            )

        # Check if the words are of equal length
        if len(start_word) != len(end_word):
            return JsonResponse(
                {"error": "Both startWord and endWord must be of the same length."},
                status=400,
            )

        # Check if the words contain only letters
        if not all(word.isalpha() for word in [start_word, end_word]):
            return JsonResponse(
                {"error": "Both startWord and endWord must be of type string."},
                status=400,
            )
