# Standard library imports
import logging

# Related third-party imports
from celery.result import AsyncResult
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Local application/library-specific imports
from .serializers import ProcessSerializer, UserRegistrationSerializer
from .tasks import process_data_task

# Logger for API-related logs
api_logger = logging.getLogger("api_logger")
# Logger for Celery task-related logs
tasks_logger = logging.getLogger("celery_tasks")


@swagger_auto_schema(
    method="post",
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response(description="User registered successfully"),
        400: openapi.Response(
            description="Bad Request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    },
    operation_summary="Register a new user",
    operation_description="This endpoint accepts user data and registers a new user.",
    security=[],  # No authentication required
)
@api_view(["POST"])
@authentication_classes([])  # No authentication required
@permission_classes([AllowAny])  # Allow any user (including unauthenticated)
def register_user(request):
    """
    Register a new user.
    This view handles user registration by accepting a POST request with
    user data, validating the data using the `UserRegistrationSerializer`,
    and then creating a user if the data is valid. It logs both successful
    and failed registration attempts.
    """
    # Initialize the serializer with incoming registration data
    serializer = UserRegistrationSerializer(data=request.data)
    # Validate and save the user data if it's valid
    if serializer.is_valid():
        serializer.save()
        api_logger.info(
            f"User registered successfully with email: {request.data.get('email')}"
        )
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )

    api_logger.error(
        f"User registration failed for email: {request.data.get('email')}. Errors: {serializer.errors}"
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=AuthTokenSerializer,
    responses={
        200: openapi.Response(
            description="Token issued successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        400: openapi.Response(
            description="Bad Request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    },
    operation_summary="Authenticate user and return token with user info",
    operation_description="This endpoint authenticates a user using credentials and returns a token along with the user's ID and email.",
    security=[],  # No authentication required to obtain token
)
@api_view(["POST"])
@authentication_classes([])  # No authentication required to obtain token
@permission_classes([AllowAny])  # Allow any user (including unauthenticated)
def custom_auth_token(request):
    """
    Authenticate user and return token with user info.
    """
    # Initialize the serializer with login credentials from the request
    serializer = AuthTokenSerializer(data=request.data)
    # If credentials are valid, retrieve the associated user
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        api_logger.info(f"Token issued for user: {user.username}")

        return Response({"token": token.key, "user_id": user.id, "email": user.email})

    api_logger.warning(f"Failed login attempt with data: {request.data}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=ProcessSerializer,
    responses={202: openapi.Response(description="Accepted"), 400: "Bad Request"},
    operation_summary="Process data asynchronously",
    operation_description="This endpoint accepts an email and message",
    security=[{"Token": []}],  #  Tells Swagger this endpoint uses Token auth
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])  # Requires token-based authentication
@permission_classes([IsAuthenticated])  # Only authenticated users can access
def process_view(request):
    """
    Process data using Celery asynchronously.
    This view accepts user input (email and message), validates it, and triggers
    a background task using Celery. It requires user authentication and logs both
    successful and failed requests.
    """
    # Initialize the serializer with the incoming request data
    serializer = ProcessSerializer(data=request.data)
    # If the data is valid, extract the email and message
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        message = serializer.validated_data["message"]
        # Trigger the Celery task asynchronously with the validated data
        task = process_data_task.delay(email, message)

        tasks_logger.info(
            f"Processing task created by {request.user.username} | Task ID: {task.id}"
        )
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

    tasks_logger.error(
        f"Failed to create processing task by {request.user.username} | Errors: {serializer.errors}"
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "task_id",
            openapi.IN_PATH,
            description="The ID of the Celery task to check status for",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            description="Task status and result",
            examples={
                "application/json": {
                    "task_id": "abcd-1234",
                    "status": "SUCCESS",
                    "result": "Processed message here",
                }
            },
        ),
        401: "Unauthorized",
    },
    operation_summary="Check Celery Task Status",
    operation_description="Returns the status and result of a background task using its task ID.",
    security=[{"Token": []}],
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_status_view(request, task_id):
    """
    Retrieve the status and result of a Celery background task using its task ID.
    Only accessible by authenticated users.
    """
    # Retrieve the asynchronous task result using its task ID
    result = AsyncResult(task_id)
    # Get the current status of the task
    task_status = result.status
    # Get the result returned by the task
    task_result = result.result

    tasks_logger.info(
        f"User {request.user.username} checked task status | Task ID: {task_id} | Status: {task_status}"
    )

    return Response(
        {"task_id": task_id, "status": task_status, "result": task_result},
        status=status.HTTP_200_OK,
    )
