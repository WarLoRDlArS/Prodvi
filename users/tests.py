from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Users

User = get_user_model()

class UserViewsTests(TestCase):
    
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            username='test_user',
            pid='123456',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_page_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_page_post_invalid_pid(self):
        response = self.client.post(reverse('users:login'), {'pid': 'wrong_pid', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after failure
        self.assertRedirects(response, reverse('users:login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid PID')

    def test_login_page_post_invalid_credentials(self):
        response = self.client.post(reverse('users:login'), {'pid': self.test_user.pid, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after failure
        self.assertRedirects(response, reverse('users:login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Credentials')

    def test_login_page_post_success(self):
        response = self.client.post(reverse('users:login'), {'pid': self.test_user.pid, 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, reverse('home:index'))

    def test_landing_page(self):
        response = self.client.get(reverse('users:landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/landing_page.html')

    def test_signup_page_get(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_page_post_password_mismatch(self):
        response = self.client.post(reverse('users:signup'), {
            'name': 'New User',
            'email': 'new@example.com',
            'pid': '654321',
            'password1': 'password123',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after failure
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Passwords should match.')

    def test_signup_page_post_invalid_pid_length(self):
        response = self.client.post(reverse('users:signup'), {
            'name': 'New User',
            'email': 'new@example.com',
            'pid': '123',  # Invalid PID length
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after failure
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'PID Length Should be Exactly 6')

    def test_signup_page_post_success(self):
        response = self.client.post(reverse('users:signup'), {
            'name': 'New User',
            'email': 'new@example.com',
            'pid': '654321',
            'password1': 'password123',
            'password2': 'password123',
            'role': 'employee'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(Users.objects.filter(pid='654321').exists())  # Check that the user was created

