import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestSelenium:

    def __init__(self):
        driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
        options = Options()
        options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("http://localhost:5000")

    def login(self):
        """user connection"""
        self.driver.get("http://localhost:5000")
        time.sleep(1)
        assert self.driver.title == "GUDLFT Registration"
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("john@simplylift.co")
        email_input.send_keys(Keys.RETURN)

        time.sleep(2)
        assert "Welcome, john@simplylift.co" in self.driver.page_source

    def booking_page(self):
        """open reservation page"""
        book_places_link = self.driver.find_element(By.LINK_TEXT, "Book Places")
        book_places_link.click()
        time.sleep(2)
        assert "Fall Classic 2025" in self.driver.page_source
        assert "Simply Lift" in self.driver.page_source

    def book_places(self):
        """book a place"""
        places_input = self.driver.find_element(By.NAME, "places")
        places_input.send_keys("1")
        places_input.send_keys(Keys.RETURN)
        time.sleep(2)
        assert "Great-booking complete!" in self.driver.page_source

    def logout(self):
        """logout from website"""
        self.driver.get("http://localhost:5000/logout")
        time.sleep(2)
        assert "Logout!" in self.driver.page_source

    def close(self):
        """close navigator"""
        self.driver.quit()


if __name__ == "__main__":
    fonctional_test = TestSelenium()

    try:
        fonctional_test.login()
        fonctional_test.booking_page()
        fonctional_test.book_places()
        fonctional_test.logout()
    finally:
        # pour être sur de fermer même si plantage
        fonctional_test.close()
