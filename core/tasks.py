# Standard library imports
import logging
import time

# Related third-party imports
from celery import shared_task
from django.db import IntegrityError

# Local application/library-specific imports
from .models import ProcessedData


# Logger for Celery task-related logs
tasks_logger = logging.getLogger("celery_tasks")
# Logger for API-related logs
api_logger = logging.getLogger("api_logger")


# Define a Celery task with hard and soft time limits to prevent runaway tasks.
@shared_task(time_limit=30, soft_time_limit=25)
def process_data_task(email, message):
    """
    Task to process data and save the result to the database.

    Args:
    - email (str): The email address to associate with the processed data.
    - message (str): The message to process.

    Returns:
    - str: Confirmation of the processed data saved or error message.
    """
    try:
        # Log the start of the task
        tasks_logger.info(
            f"Starting task to process data for email: {email} with message: '{message}'"
        )

        # Simulate data processing: Convert message to uppercase (simple transformation)
        processed_message = message.upper()  # Example of data transformation

        # Simulate a time-consuming operation
        time.sleep(5) 

        # Save processed data to the database
        processed_data = ProcessedData.objects.create(
            email=email, original_message=message, processed_message=processed_message
        )

        # Log the successful processing of data
        tasks_logger.info(f"Processed data for email: {email}, stored in database.")

        return f"Data processed and saved successfully for email: {email}"

    except IntegrityError as e:
        # Handle specific database errors, like duplicate entries or constraints violations
        api_logger.error(
            f"Database error while processing data for email: {email}. Error: {str(e)}"
        )
        return (
            f"Database error while processing data for email: {email}. Error: {str(e)}"
        )

    except Exception as e:
        # Catch any unexpected errors and log them
        tasks_logger.error(f"Error processing data for email: {email}. Error: {str(e)}")
        return f"Error processing data for email: {email}. Error: {str(e)}"
