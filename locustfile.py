import time
from locust import HttpUser, task, between
class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_teams_for_user(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJGSU8iOiJzdHJpbmciLCJpc0FkbWluIjp0cnVlLCJpc0N1cmF0b3IiOnRydWUsImlzVGVhY2hlciI6dHJ1ZSwidXNlcm5hbWUiOiJzdHJpbmciLCJwYXNzd29yZCI6IiQyYiQxMiRRVlN4QVIwRDNNbEJuUEdNZFoxWEUuTmE2aE1HaGZIdzE3RlU4UmE3aElHcEFSL3pVLnR2cSIsImVtYWlsIjoic3RyaW5nIiwiZXhwIjoxNzA5NTgxNjc0fQ.2yi-9sMcQWJXIX6ELSQED82FB30173g-jvJp4y8MaD0"  # Replace with the actual token
        response = self.client.get(f"/api/get_teams_for_user?token={token}")

        # print(response.status_code)
        # print(response.json())