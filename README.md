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
* **Student Service:** `ananyaabhat/student-service:latest`
* **Internship Service:** `bhagyashree028/internship-service:v1`
* **Application Service:** `priya721k/application-service:v1`

#### Pull pre-built images from Docker Hub:
```bash
docker pull ananyaabhat/student-service:latest
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
| **W1** | 1 | 7.98 | 3 | 0 | 2.10 | 53.17 |
| **W2** | 2 | 8.95 | 6.9 | 0 | 2.98 | 53.9 |
| **W3** | 4 | 9.15 | 11.6 | 0 | 4.94 | 55.03 |
| **W4** | 8 | 9.41 | 25.7 | 0 | 11.11 | 54.98 |
| **W5** | 16 | 10.51 | 50.4 | 0 | 16.31 | 54.16 |

#### W1: 1 concurrent user
<img width="1920" height="1020" alt="Screenshot 2026-10-04 135459" src="https://github.com/user-attachments/assets/9e520ccb-3c1d-4206-963e-5774c4079a4f" />
<img width="592" height="175" alt="Screenshot 2026-10-04 140128" src="https://github.com/user-attachments/assets/61ec8355-de01-41ad-b558-a809311e78ed" />

#### W2: 2 concurrent user
<img width="1916" height="540" alt="image" src="https://github.com/user-attachments/assets/2faf3ebe-0960-4f9b-b7b1-c0bed8920f69" />
<img width="943" height="280" alt="Screenshot 2026-10-04 135938" src="https://github.com/user-attachments/assets/3d04e4c3-4c6c-47c0-a684-89ecdcb0d298" />

#### W3: 4 concurrent user
<img width="1917" height="515" alt="image" src="https://github.com/user-attachments/assets/50f813c8-935f-4e46-bcab-230d3f1eb663" />
<img width="955" height="287" alt="image" src="https://github.com/user-attachments/assets/7407b04e-59e8-4d8e-ac50-f0bfae3c1c3b" />

#### W4: 8 concurrent user
<img width="1916" height="571" alt="image" src="https://github.com/user-attachments/assets/9e4799b9-d0ad-4610-9b86-7d40a810bc92" />
<img width="962" height="265" alt="image" src="https://github.com/user-attachments/assets/f333276b-0f40-452d-a14f-c54b5e86faa8" />

#### W5: 16 concurrent user
<img width="1917" height="501" alt="image" src="https://github.com/user-attachments/assets/831f915c-2a94-47e8-9f09-424dedf5fa90" />
<img width="958" height="286" alt="image" src="https://github.com/user-attachments/assets/e57ba2db-17ff-4b1f-8ee2-4e10033f6425" />



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
## Key Performance Insights
1. Throughput Scales Linearly with ConcurrencyAs concurrent users increase from 1 (W1) to 16 (W5), throughput increases nearly 17x (from 3 RPS to 50.4 RPS).   This shows that your FastAPI microservice stack and Docker network handle concurrent requests efficiently without hitting a early performance bottleneck.
2. Extremely Low Latency DegradationAverage response time remains virtually flat, increasing by only ~2.5 ms under 16x load (from 7.98 ms at W1 to 10.51 ms at W5).   The asynchronous nature of FastAPI/Uvicorn allows request queuing and execution to stay highly responsive under load.  
3.  Resource Utilization EfficiencyCPU Utilization: Scales predictably with request volume, rising from 2.10% at baseline up to 16.31% at 16 concurrent users.   Memory Utilization: Remains exceptionally stable around ~53–55 MB across all test runs. SQLite in memory/file mode combined with lightweight Python processes keeps the overall container footprint minimal.
4. Zero Failures Across All WorkloadsFailed Requests = 0 across all 5 test levels, demonstrating 100% service availability and stability under load.  



---

## Git Workflow

```bash
git status
git add .
git commit -m "Update microservice stack"
git push origin main
```



