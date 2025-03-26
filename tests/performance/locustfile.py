from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def create_user(self):
        self.client.post("/users", json={"username": "testuser", "password": "secure123"})