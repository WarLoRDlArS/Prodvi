from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class SignupPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        cls.base_url = 'http://localhost:8000'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_page_loads(self):
        self.driver.get(self.base_url + '/signup/')
        self.assertEqual(self.driver.title, "Signup Page")

        name_input = self.driver.find_element(By.NAME, 'name')
        self.assertIsNotNone(name_input)

        email_input = self.driver.find_element(By.NAME, 'email')
        self.assertIsNotNone(email_input)

        pid_input = self.driver.find_element(By.NAME, 'pid')
        self.assertIsNotNone(pid_input)

        password1_input = self.driver.find_element(By.NAME, 'password1')
        self.assertIsNotNone(password1_input)

        password2_input = self.driver.find_element(By.NAME, 'password2')
        self.assertIsNotNone(password2_input)

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertIsNotNone(submit_button)

    def test_successful_signup(self):
        self.driver.get(self.base_url + '/signup/')

        name_input = self.driver.find_element(By.NAME, 'name')
        name_input.send_keys("Test User")

        email_input = self.driver.find_element(By.NAME, 'email')
        email_input.send_keys("test@example.com")

        pid_input = self.driver.find_element(By.NAME, 'pid')
        pid_input.send_keys("999999")

        password1_input = self.driver.find_element(By.NAME, 'password1')
        password1_input.send_keys("abc")

        password2_input = self.driver.find_element(By.NAME, 'password2')
        password2_input.send_keys("abc")

        role_select = self.driver.find_element(By.NAME, 'role')
        role_select.click()
        role_select.find_element(By.XPATH, "//option[@value='employee']").click()

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        self.assertEqual(self.driver.current_url, self.base_url + '/login/')
