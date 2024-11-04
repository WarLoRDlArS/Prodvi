from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class LoginPageTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        cls.driver = webdriver.Firefox()
        cls.base_url = 'http://localhost:8000'
        cls.driver.implicitly_wait(5)  # Implicit wait for elements to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def login(self, pid, password):
        """Helper function to perform login with given pid and password."""
        self.driver.get(self.live_server_url + '/login/')
        self.driver.find_element(By.NAME, 'pid').clear()
        self.driver.find_element(By.NAME, 'pid').send_keys(pid)
        self.driver.find_element(By.NAME, 'password').clear()
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click() 


    def test_invalid_login_empty_fields(self):
        """Test login with empty pid and password fields."""
        self.driver.get(self.base_url + '/login/')
        self.login('', '')  # Assuming this method submits the form

        # Wait for the error message to be present
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
            ).text
            self.assertIn("PID is required", error_message)
        except:
            self.fail("Error message not found after form submission.")

    def test_invalid_login_short_pid(self):
        """Test login with pid that is too short (BVA - boundary condition)."""
        self.login('222', 'larson')
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid PID", error_message)

    def test_invalid_login_long_pid(self):
        self.driver.get(self.base_url + '/login/')
        
        # Enter a PID that is too long
        self.driver.find_element(By.NAME, 'pid').send_keys('1234567')  # Example of long PID
        self.driver.find_element(By.NAME, 'password').send_keys('password')  # Any password
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the error message to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )

        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid PID", error_message)

    def test_invalid_login_wrong_credentials(self):
        self.driver.get(self.base_url + '/login/')
        
        # Enter valid PID but wrong password
        self.driver.find_element(By.NAME, 'pid').send_keys('000000')  # Example of valid PID
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpassword')  # Wrong password
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the error message to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )

        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid Credentials", error_message)
