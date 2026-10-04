from locust import HttpUser, task, between, events

class AuthenticatedUser(HttpUser):
    # Wait between 0.1 and 0.5 seconds between tasks
    wait_time = between(0.1, 0.5)
    token = None

    def on_start(self):
        """
        Runs automatically ONCE for every simulated user when spawned.
        Logs in and stores the access token in headers.
        """
        login_payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        
        # Request access token from authentication endpoint
        response = self.client.post("/auth/login", json=login_payload)
        
        if response.status_code == 200:
            token_data = response.json()
            # Extract access_token (adjust key depending on your API response model)
            self.token = token_data.get("access_token")
            # Set Authorization header for all subsequent HTTP calls from this user
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            response.failure(f"Failed to authenticate user: {response.status_code}")

    @task(3)
    def test_protected_list_applications(self):
        """
        Benchmark GET /applications (Protected route)
        Automatically passes the Bearer token set in on_start.
        """
        self.client.get("/applications")

    @task(2)
    def test_protected_get_user_profile(self):
        """
        Benchmark GET /auth/me or protected user endpoint
        """
        self.client.get("/auth/me")

    @task(1)
    def test_public_health_check(self):
        """
        Benchmark GET / endpoint (Public route)
        """
        self.client.get("/")