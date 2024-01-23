# urls.py
from django.urls import path

from .views import WordPuzzleApi

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="WordPuzzle API",
        default_version="v1",
        description="API for WordPuzzle",
        contact=openapi.Contact(email="anuragverma65@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Allow any user to access Swagger
)
urlpatterns = [
    path("wordpuzzle", WordPuzzleApi.as_view(), name="wordpuzzle"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
