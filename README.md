# Internship Management System

A simple **microservices-based Internship Management System** built using **FastAPI, SQLite, Docker, and Docker Compose**.

The project is divided into four independent services. Each service has its own application, Docker image, and SQLite database.

## Services

| Service             | Purpose                        | Port |
| ------------------- | ------------------------------ | ---: |
| Auth Service        | User registration and login    | 8001 |
| Student Service     | Manage student information     | 8002 |
| Internship Service  | Manage internship details      | 8003 |
| Application Service | Manage internship applications | 8004 |

Each service runs independently in its own Docker container.

## Architecture

```text
                    Internship Management System
                              |
          -------------------------------------------
          |          |           |                  |
       Auth       Student    Internship       Application
      Service      Service      Service          Service
          |          |           |                  |
       auth.db    students.db  internships.db  applications.db
          |          |           |                  |
       Docker     Docker       Docker           Docker
       Volume     Volume       Volume           Volume
```

## Project Structure

```text
internship-management-sqlite/
│
├── auth-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── student-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── internship-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── application-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Docker
* Docker Compose
* Git
* GitHub
* Docker Hub

## Prerequisites

Install the following on your system:

* Git
* Docker Desktop

Check the installations:

```bash
git --version
docker --version
docker compose version
```

## Run Using Docker Compose

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Go into the project directory:

```bash
cd internship-management-sqlite
```

Start all services:

```bash
docker compose up --build
```

The four containers will start together.

### API Documentation

FastAPI provides interactive Swagger documentation for each service.

**Auth Service**

http://localhost:8001/docs

**Student Service**

http://localhost:8002/docs

**Internship Service**

http://localhost:8003/docs

**Application Service**

http://localhost:8004/docs

You can use these pages to test the APIs directly from the browser.

## Docker Containers

After starting the project, check the running containers:

```bash
docker ps
```

You should see four containers corresponding to:

```text
auth
student
internship
application
```

To stop the containers:

```bash
docker compose down
```

To stop the containers and delete the SQLite volumes:

```bash
docker compose down -v
```

> `docker compose down -v` permanently removes the databases stored in the Docker volumes.

## Docker Hub Images

Docker images for the individual services are also available on Docker Hub.

Docker Hub username:

```text
bhagyashree028
```

Images:

```text
bhagyashree028/auth-service:v1
bhagyashree028/student-service:v1
bhagyashree028/internship-service:v1
bhagyashree028/application-service:v1
```

The images can be pulled using:

```bash
docker pull bhagyashree028/auth-service:v1
docker pull bhagyashree028/student-service:v1
docker pull bhagyashree028/internship-service:v1
docker pull bhagyashree028/application-service:v1
```

The current `docker-compose.yml` builds the services from their Dockerfiles using:

```bash
docker compose up --build
```

## Example API Usage

### 1. Register a User

Open the Auth Service:

```text
http://localhost:8001/docs
```

Use:

```http
POST /register
```

Example:

```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "password": "demo123"
}
```

### 2. Login

```http
POST /login
```

Example:

```json
{
  "email": "asha@example.com",
  "password": "demo123"
}
```

### 3. Create a Student

Open:

```text
http://localhost:8002/docs
```

Use:

```http
POST /students
```

Example:

```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "department": "CSE",
  "year": 3
}
```

### 4. Create an Internship

Open:

```text
http://localhost:8003/docs
```

Use:

```http
POST /internships
```

Example:

```json
{
  "title": "Backend Intern",
  "company": "Example Ltd",
  "location": "Remote",
  "description": "Python backend internship"
}
```

### 5. Apply for an Internship

Open:

```text
http://localhost:8004/docs
```

Use:

```http
POST /applications
```

Example:

```json
{
  "student_id": 1,
  "internship_id": 1
}
```

### 6. Update Application Status

```http
PATCH /applications/1/status
```

Example:

```json
{
  "status": "accepted"
}
```

Allowed statuses:

```text
pending
accepted
rejected
```

## Database and Volumes

Each service has its own SQLite database.

```text
Auth Service          → auth.db
Student Service       → students.db
Internship Service    → internships.db
Application Service   → applications.db
```

Docker Compose creates separate named volumes:

```text
auth_data
student_data
internship_data
application_data
```

This allows the data to remain available even when the containers are stopped and restarted.

## Useful Docker Commands

View running containers:

```bash
docker ps
```

View all containers:

```bash
docker ps -a
```

View images:

```bash
docker images
```

View logs of all services:

```bash
docker compose logs
```

View logs of one service:

```bash
docker compose logs auth
```

Restart the project:

```bash
docker compose restart
```

Stop the project:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

## Git Workflow

Basic Git workflow used for this project:

```bash
git status
git add .
git commit -m "Update project"
git push
```

To get the latest changes from GitHub:

```bash
git pull
```

## How the Project Works

Each service is an independent FastAPI application.

```text
Client
  |
  |----> Auth Service
  |
  |----> Student Service
  |
  |----> Internship Service
  |
  |----> Application Service
```

Each service:

1. Has its own FastAPI application.
2. Has its own Dockerfile.
3. Has its own Python dependencies.
4. Runs inside its own container.
5. Uses its own SQLite database.
6. Stores database data in a Docker volume.

Docker Compose is used to start all four services together.

## Learning Objectives

This project was created to understand the basics of:

* Microservice architecture
* FastAPI services
* REST APIs
* Dockerfiles
* Docker images
* Docker containers
* Docker volumes
* Docker Compose
* Docker Hub
* Git and GitHub
* Running multiple services together



