# Standard library imports
import uuid

# Related third-party imports
from django.db import models


class Process(models.Model):
    """
    Represents a processing step involving a user's email and message.

    Attributes:
        email (EmailField): The email of the user.
        message (CharField): The message associated with the process.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    message = models.CharField(max_length=255)

    def __str__(self):
        # Returns a string representation of the Process instance.
        return self.email


class ProcessedData(models.Model):
    """
    Stores information about processed messages, including the original input,
    the processed result, and a timestamp of when the processing occurred.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # UUID as primary key
    email = models.EmailField()
    original_message = models.TextField()
    processed_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Returns a string representation of the Process data instance.
        return f"Processed data for {self.email} at {self.created_at}"
