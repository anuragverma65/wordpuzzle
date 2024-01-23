from django.http import JsonResponse
from rest_framework.views import APIView

from .models import WordPuzzle

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from drf_yasg import openapi


class WordPuzzleApi(APIView):
    @swagger_auto_schema(
        operation_description="Get word puzzle result",
        manual_parameters=[
            openapi.Parameter(
                "startWord",
                in_=openapi.IN_QUERY,
                description="Start word",
                required=True,
                example="oyster",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "endWord",
                in_=openapi.IN_QUERY,
                description="End word",
                required=True,
                example="mussel",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                        )
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(type=openapi.TYPE_STRING),
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal server error",
                schema=openapi.Schema(type=openapi.TYPE_STRING),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        start_word = request.GET.get("startWord", "")
        end_word = request.GET.get("endWord", "")

        # Check if the result is already saved in the database
        saved_result = WordPuzzle.objects.filter(
            start_word=start_word, end_word=end_word
        ).first()
        if saved_result:
            # Return the saved result directly
            sequence = saved_result.sequence.split(",") if saved_result.sequence else []
        else:
            # Perform the word transformation search using your search logic
            sequence = WordPuzzle().shortest_sequence(start_word, end_word)

            # Save the search request to the database
            WordPuzzle.objects.create(
                start_word=start_word,
                end_word=end_word,
                sequence=",".join(map(str, sequence)),
            )

        return JsonResponse({"data": sequence})
