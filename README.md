# Poll App

Poll App is a web application that allows users to create polls, vote on them, and view results in real time. This project leverages Django, PostgreSQL, Docker, and GitHub Actions for CI/CD.

## Features

- Create new polls with multiple options.
- Vote on existing polls.
- View poll results.
- Real-time updates on poll results.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- Docker
- Docker Compose
- PostgreSQL

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Mark-hil/poll_app.git
   cd poll_app
2. **Create Environment Variables**
Create a .env file in the root directory and add the following:

3. **Build and Run with Docker Compose**
  ```bash
   docker-compose up --build


3. Build and Run with Docker Compose
sh
docker-compose up --build
4. Run Migrations
sh
docker-compose exec web python manage.py migrate
Running Tests
To run tests, use the following command:

sh
docker-compose exec web python manage.py test
Deployment
This project uses GitHub Actions for CI/CD. On every push to the main branch, the workflow will:

Build the Docker image.

Run tests.

Push the Docker image to Docker Hub if all tests pass.
