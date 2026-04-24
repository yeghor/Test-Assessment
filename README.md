# Test Assessment

This is a test assessment project, implementing a traveling backend service using FastAPI. The application allows users to create and manage travel projects, including adding and organizing places using external APIs.

> Access Swagger API is available at `http://localhost:8000` after project startup


## Prerequisites

- Docker
- Git (for cloning the repository)
- Python 3.11+

## Installation

1. Clone the repository:

   ```bash
   git clone 
   cd Test-Assesment
   ```

## Running the Project

To start the project using Docker:

1. Build the Docker image:
   ```bash
   docker build -t traveling_backend .
   ```

2. Run the container:

   ```bash
   docker run --name traveling_backend_container -p 8000:8000 -d traveling_backend
   ```

The application will be available at `http://localhost:8000`


To see Swagger docs, navigate at `http://localhost:8000/docs`

## Development

For local development:

1. Install dependencies:
   ```bash
   cd backend
   pip install -e .
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The application will be available at `http://localhost:8000`

To see Swagger docs, navigate at `http://localhost:8000/docs`
