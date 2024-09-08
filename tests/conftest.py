import pytest

from main_app import create_app

@pytest.fixture
def first_fixture():
    data = {"first_name": "Ranga",
            "name": "Gonnage"}
    return data

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


class TestClass:
    def setup_method(self, method):
        print("--> Setup method")

    def teardown_method(self, method):
        print("\n--> Teardown method")

    def test_one(self):
        print("--> Run first test")
