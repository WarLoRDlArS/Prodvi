from django.urls import reverse
from django.test import override_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@override_settings(DEBUG=True)  # Ensures more helpful error output in tests
class AddNoticeSeleniumTest(TestCase):
    def setUp(self):
        # Set up your test data
        self.driver = webdriver.Firefox()  # Or use Chrome depending on your setup
        self.driver.implicitly_wait(10)  # Waits up to 10 seconds for elements to load

        # Create a test manager user and employee profile
        self.manager_user = Users.objects.create_user(pid='222104', password='testpassword', username='manageruser', role='manager')
        self.manager_employee = Employee.objects.create(user=self.manager_user, is_manager=True)

        # Set up a test group with employees
        self.test_group = Group.objects.create(name="Test Group")
        self.test_group.managers.add(self.manager_employee)

        # Add employees to the group
        self.employee1 = Users.objects.create_user(pid='555555', password='testpassword', username='empuser1', role='manager')
        Employee.objects.create(user=self.employee1)
        self.employee2 = Users.objects.create_user(pid='626262', password='testpassword', username='empuser2', role='manager')
        Employee.objects.create(user=self.employee2)
        self.test_group.employees.set([self.employee1, self.employee2])

    def tearDown(self):
        self.driver.quit()

    def test_add_notice(self):
        # Log in as the manager user
        self.driver.get(self.live_server_url + reverse('users:login'))
        self.driver.find_element(By.NAME, 'pid').send_keys('managerpid')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Navigate to add notice page
        self.driver.get(self.live_server_url + reverse('home:add_notice'))

        # Fill out notice form fields (assuming form has a title and message field)
        self.driver.find_element(By.NAME, 'title').send_keys("Test Notice Title")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test notice message.")

        # Select a group from the dropdown
        group_dropdown = self.driver.find_element(By.NAME, 'group_id')
        for option in group_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == "Test Group":
                option.click()
                break

        # Enter comma-separated PIDs for direct assignment
        self.driver.find_element(By.NAME, 'pids').send_keys('emp1pid, emp2pid')

        # Submit the form
        self.driver.find_element(By.XPATH, '//button[text()="Submit Notice"]').click()

        # Wait and check if the assigned users appear in the notice list
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h4[text()="Assigned Users:"]'))
        )
        assigned_users = self.driver.find_elements(By.CSS_SELECTOR, '.list-group-item')
        assigned_user_pids = [user.text.split('-')[0].strip() for user in assigned_users]

        # Validate assigned users include all PIDs
        self.assertIn('emp1pid', assigned_user_pids)
        self.assertIn('emp2pid', assigned_user_pids)

