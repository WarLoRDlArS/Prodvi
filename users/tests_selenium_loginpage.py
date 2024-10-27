from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class LoginPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server_url = 'http://127.0.0.1:8000'  # Point to your running local server
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_page_loads(self):
        self.driver.get(self.server_url + '/users/login/')
        self.assertEqual(self.driver.title, "Login Page")

        pid_input = self.driver.find_element(By.NAME, 'pid')
        self.assertIsNotNone(pid_input)

        password_input = self.driver.find_element(By.NAME, 'password')
        self.assertIsNotNone(password_input)

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertIsNotNone(submit_button)

    def test_successful_login(self):
        self.driver.get(self.server_url + '/users/login/')
        self.driver.find_element(By.NAME, 'pid').send_keys('100000')
        self.driver.find_element(By.NAME, 'password').send_keys('larson')
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        self.assertEqual(self.driver.current_url, self.server_url + '/home/index/')
        self.assertIn("Welcome", self.driver.page_source)

    def test_login_with_invalid_credentials(self):
        self.driver.get(self.server_url + '/users/login/')
        self.driver.find_element(By.NAME, 'pid').send_keys('999999')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpassword')
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        error_message = self.driver.find_element(By.CLASS_NAME, 'messages')
        self.assertIn("Invalid credentials", error_message.text)

    def test_display_message_on_password_mismatch(self):
        self.driver.get(self.server_url + '/users/signup/')
        self.driver.find_element(By.NAME, 'pid').send_keys('100001')
        self.driver.find_element(By.NAME, 'password').send_keys('password123')
        self.driver.find_element(By.NAME, 'confirm_password').send_keys('differentpassword')
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        error_message = self.driver.find_element(By.CLASS_NAME, 'messages')
        self.assertIn("Password Should be Same", error_message.text)
