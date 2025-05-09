# Microservice Project

This project is a Django-based microservice application that uses Docker for containerization. It includes functionality for token-based authentication, background task processing using Celery, and integrates with PostgreSQL for database storage and Redis for caching and message brokering. The project also includes Swagger API documentation.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Architecture](#2-architecture)
   - [Services](#services)
   - [Dependencies](#dependencies)
   - [Security](#security)
3. [Running the Application](#3-running-the-application)
4. [Testing the Application](#4-testing-the-application)
5. [Docker Configuration](#5-docker-configuration)
6. [Environment Variables](#6-environment-variables)

---

## 1. Project Setup

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Python** (for local development, if needed).
- **PostgreSQL** and **Redis** (Docker will handle these dependencies).

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EkeneDeProgram/django-aws-deployment.git
   cd microservice

2. **Create a .env file for environment variables**:
    - Duplicate the **.env.example** and rename it to **.env**.
    - Fill in the necessary environment variables for your setup **(e.g., DEBUG, ALLOWED_HOSTS, etc.)**.

3. **Build and start the Docker containers**:
To build and start the application along with its services (PostgreSQL, Redis, Celery), run the following command:
```bash
docker-compose up --build
```

4. **Apply Migrations**:
After starting the containers, run the migrations to set up the database:
```bash
docker-compose exec web python manage.py migrate
```

## 2. Architecture

### Services

The application is divided into multiple services, each performing a specific role:

- **Web Service (Django + Gunicorn)**:  
  This is the main application server that runs the Django application using Gunicorn. It is responsible for serving HTTP requests and serving API documentation (Swagger).

- **PostgreSQL Database (db)**:  
  The PostgreSQL service stores application data, such as user credentials and other microservice-related data.

- **Redis (redis)**:  
  Used for caching and message brokering, Redis facilitates the asynchronous processing of background tasks using Celery.

- **Celery Worker (celery)**:  
  This service is responsible for running background tasks, such as data processing and sending emails. Celery works with Redis as the message broker.


### Dependencies

- **Django**:  
  The main web framework used in the project.

- **drf-yasg**:  
  A library for automatically generating interactive API documentation (Swagger).

- **Celery**:  
  A task queue used to handle background tasks asynchronously.

- **PostgreSQL**:  
  A relational database for storing application data.

- **Redis**:  
  A key-value store used as a message broker for Celery.

- **Gunicorn**:  
  A Python WSGI HTTP Server for running the Django application.

- **djangorestframework (DRF)**:  
  Provides a toolkit for building Web APIs in Django.

### Security

- **Token Authentication**:  
  The API requires token-based authentication. Token generation and management can be handled using Django Rest Framework's `TokenAuthentication`.

- **Swagger UI**:  
  The Swagger UI is publicly accessible for testing and viewing the API endpoints. If you want to restrict access to authenticated users, you can change the permission classes in the schema view.

## 3. Running the Application

To run the application locally, follow these steps:

1. **Build and Start Docker Containers:**:
```bash
   docker-compose up --build
```
2. **Access Swagger API Documentation**:
Open your browser and go to the following URL to access the Swagger UI:
```bash
   http://localhost:8000/swagger/
```
3. **Access the Application**:
The API will be available at:
```bash 
   http://localhost:8000/
```

## 4. Testing the Application

To interact with the application and test the endpoints, follow these steps:

1. **Obtain a  Token**:
   - Obtain a token by logging using this endpoint (`/api/login/`) after registration through this endpoint (`/api/register/`).

2. **Authorize via Swagger UI**:
   - Navigate to the Swagger UI page at `http://localhost:8000/swagger/`.
   - Click the **Authorize** button.
   - Enter your token in the following format:
     ```
     Token <your_token>
     ```

3. **Test Endpoints**:
Use the Swagger UI to test various API endpoints. You can send POST requests, view responses, and check status codes.


## 5. Docker Configuration

The project uses Docker to containerize the application and its dependencies. Here's a quick overview of the Docker-related files:

- **Dockerfile**: Defines how to build the Docker image for the web application.
- **docker-compose.yml**: Defines the services (Web, PostgreSQL, Redis, Celery) and how they interact with each other.

### To run the app with Docker Compose:

```bash
docker-compose up --build
```
This will build the images (if not already built), start the containers, and attach the logs.

## 6. Environment Variables

The `.env.example` file contains the necessary environment variables for the project. Copy this file to `.env` and configure it as needed.

### Example `.env` file:

```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
SECRET_KEY=your-django-secret-key
```
