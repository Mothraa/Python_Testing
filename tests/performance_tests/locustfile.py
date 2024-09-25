from locust import HttpUser, TaskSet, task, between


class BookingTest(TaskSet):

    def on_start(self):
        """Called on start by each user"""
        self.email = 'john@simplylift.co'
        self.competition_name = 'Fall Classic 2025'
        self.club_name = 'Simply Lift'
        self.login()

    def login(self):
        """identification and load welcome page"""
        with self.client.post('/showSummary', data={'email': self.email}, catch_response=True) as response:
            if b'Welcome, john@simplylift.co' in response.content:
                response.success()
            else:
                response.failure("Login failed")

    @task(1)
    def index(self):
        """load homepage"""
        with self.client.get('/', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to load index page: {response.status_code}")

    @task(3)
    def booking_page(self):
        """load booking page"""
        with self.client.get(f'/book/{self.competition_name}/{self.club_name}', catch_response=True) as response:
            if response.status_code == 200 and bytes(self.competition_name, 'utf-8') in response.content:
                response.success()
            else:
                response.failure("Booking page failed to load")

    @task(3)
    def book_places(self):
        """book places"""
        with self.client.post('/purchasePlaces', data={
            'club': self.club_name,
            'competition': self.competition_name,
            'places': 1
        }, catch_response=True) as response:
            if response.status_code == 200 and b'Great-booking complete!' in response.content:
                response.success()
            else:
                response.failure("Failed to book places")

    @task(1)
    def logout(self):
        """user logout"""
        with self.client.get('/logout', catch_response=True) as response:
            if response.status_code == 200 and b'Logout!' in response.content:
                response.success()
            else:
                response.failure("Logout failed")


class WebsiteUser(HttpUser):
    tasks = [BookingTest]
    wait_time = between(1, 3)
    host = "http://localhost:5000"
