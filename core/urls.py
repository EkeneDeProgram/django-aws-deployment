# Related third-party imports
from django.urls import path

# Local application/library-specific imports
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register_user"),
    path("login/", views.custom_auth_token, name="login_user"),
    path("process/", views.process_view, name="process"),
    path("task-status/<str:task_id>/", views.task_status_view, name="task-status"),
]
