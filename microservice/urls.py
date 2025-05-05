from django.contrib import admin
from django.urls import path, include
from swagger.schema_view import schema_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

# Add this so static files like swagger-ui.css load in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
