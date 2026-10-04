# Internship Management System

A simple **microservices-based Internship Management System** built using **FastAPI, SQLite, Docker, and Docker Compose**.

The project is divided into three independent services. Each service has its own application, Docker image, and SQLite database.

## Services

| Service             | Purpose                        | Port |
| ------------------- | ------------------------------ | ---: |
| Student Service     | Manage student information     | 8002 |
| Internship Service  | Manage internship details      | 8003 |
| Application Service | Manage internship applications | 8004 |

Each service runs independently in its own Docker container.

## Architecture

```text
                    Internship Management System
                                 |
                  -------------------------------
                  |              |              |                  
               Student       Internship    Application
               Service        Service        Service
                  |              |              |                  
             students.db   internships.db  applications.db
                  |              |              |                  
               Docker         Docker         Docker
               Volume         Volume         Volume
```


## Project Structure

```text
CC-03-Internship-Management/
├── application-service/
│   ├── __pycache__/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── internship-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── student-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── .env
├── docker-compose.yml
├── locustfile.py
└── README.md

```

## Technologies Used

* **Language & Framework:** Python, FastAPI, Pydantic, SQLAlchemy
* **Database & Persistence:** SQLite, Docker Named Volumes
* **Containerization & Orchestration:** Docker, Docker Compose
* **Version Control & Registry:** Git, GitHub, Docker Hub
* **Workload Testing:** Locust

---

## Prerequisites

Ensure the following tools are installed on your host system:
* Git
* Docker Desktop

### Verify Installations

```bash
git --version
docker --version
docker compose version
```

---

## Checkpoint 1: Design and Develop the Microservices

Each service is an independent FastAPI application with dedicated endpoints and isolated SQLite persistence.

### API Specifications & Interactive Documentation

* **Student Service API:** [http://localhost:8002/docs](http://localhost:8002/docs)
* **Internship Service API:** [http://localhost:8003/docs](http://localhost:8003/docs)
* **Application Service API:** [http://localhost:8004/docs](http://localhost:8004/docs)

### Sample Endpoints & Payloads

#### 1. Register Student (`POST /students`)
```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "department": "CSE",
  "year": 3
}
```

#### 2. Create Internship Listing (`POST /internships`)
```json
{
  "title": "Backend Intern",
  "company": "Example Ltd",
  "location": "Remote",
  "description": "Python backend internship"
}
```

#### 3. Submit Application (`POST /applications`)
```json
{
  "student_id": 1,
  "internship_id": 1
}
```

#### 4. Update Application Status (`PATCH /applications/{id}/status`)
```json
{
  "status": "accepted"
}
```
> **Note:** Allowed statuses are `pending`, `accepted`, and `rejected`.

---

## Checkpoint 2: Containerize and Deploy the Application

Each service contains its own `Dockerfile` and builds into a standalone image.

### Docker Hub Image Repositories
* **Student Service:** `ananyaabhat/student-service:v1`
* **Internship Service:** `bhagyashree028/internship-service:v1`
* **Application Service:** `priya721k/application-service:v1`

#### Pull pre-built images from Docker Hub:
```bash
docker pull ananyaabhat/student-service:v1
docker pull bhagyashree028/internship-service:v1
docker pull priya721k/application-service:v1
```

### Deployment via Docker Compose

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd CC-03-Internship-Management
   ```

2. Launch all microservices:
   ```bash
   docker compose up --build -d
   ```

3. Verify running containers:
   ```bash
   docker ps
   ```

---

## Checkpoint 3: Establish and Demonstrate Microservice Communication

Inter-service communication is enabled through a dedicated Docker bridge network created automatically by Docker Compose.

```
 Client Request
       │
       ▼
┌──────────────┐      Internal HTTP       ┌──────────────┐
│ Application  ├─────────────────────────►│   Student    │
│   Service    │  http://student:8000/    │   Service    │
│  (Port 8004) │                          └──────────────┘
│              │      Internal HTTP       ┌──────────────┐
│              ├─────────────────────────►│  Internship  │
│              │ http://internship:8000/  │   Service    │
└──────────────┘                          └──────────────┘
```

* **Service Discovery:** Microservices reference each other using container service names (`http://student:8000` and `http://internship:8000`) instead of hardcoded local IP addresses.
* **End-to-End Flow:** When creating an application via `POST /applications`, the `application-service` validates `student_id` and `internship_id` across the internal network before persisting the entry.

---

## Checkpoint 4: Generate Varying Workloads and Monitor Performance

Load testing is conducted against target service endpoints using **Locust** while concurrently tracking resource consumption via `docker stats`.

### Execution Steps

1. Start the container stack:
   ```bash
   docker compose up -d
   ```

2. Run Locust against the Application Service:
   ```bash
   locust -f locustfile.py --host http://localhost:8004
   ```

3. Open [http://localhost:8089](http://localhost:8089) in your browser and execute tests across 5 concurrency levels (1, 2, 4, 8, and 16 concurrent users).

4. Monitor CPU and Memory metrics in real time:
   ```bash
   docker stats
   ```

### Performance Observation Table

| Workload Level | Concurrent Requests | Avg Response Time (ms) | Throughput (RPS) | Failed Requests | CPU Utilization (%) | Memory Utilization (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | 1 | | | | | |
| **W2** | 2 | | | | | |
| **W3** | 4 | | | | | |
| **W4** | 8 | | | | | |
| **W5** | 16 | | | | | |

---

## Checkpoint 5: Analyze and Present the Results

### Data Persistence & Volume Management

Each microservice maintains data isolation via dedicated SQLite databases and Docker named volumes:

```
Student Service        ──► students.db     ──► Volume: student_data
Internship Service     ──► internships.db  ──► Volume: internship_data
Application Service    ──► applications.db ──► Volume: application_data
```

### Useful Management Commands

* **View container logs:**
  ```bash
  docker compose logs -f
  ```
* **View logs for a single service:**
  ```bash
  docker compose logs application
  ```
* **Restart container stack:**
  ```bash
  docker compose restart
  ```
* **Stop containers while preserving volume data:**
  ```bash
  docker compose down
  ```
* **Tear down environment and delete database volumes:**
  ```bash
  docker compose down -v
  ```

---

## Git Workflow

```bash
git status
git add .
git commit -m "Update microservice stack"
git push origin main
```



