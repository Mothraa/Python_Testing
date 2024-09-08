from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/home")

    @task(3)
    def login(self):
        response = self.client.get("/user/login")
