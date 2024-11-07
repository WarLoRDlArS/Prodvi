from django.test import TestCase
from django.urls import reverse
from .models import Forms, Questions
from .forms import FeedbackForm  # Adjust according to your project structure
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateFeedbackFormViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            pid='100001'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_create_feedback_form_success(self):
        url = reverse('home:createfeedbackform')
        data = {
            'title': 'Test Feedback Form',
            'status': 'fresh',
            'question_text_1': 'What do you think?',
            'question_type_1': 'text',  # Text question
            'question_text_2': 'Rate your experience',
            'question_type_2': 'numeric',
            'min_value_2': '1',
            'max_value_2': '5'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Forms.objects.filter(title='Test Feedback Form').exists())
        self.assertTrue(Questions.objects.filter(question_text='What do you think?').exists())
        self.assertTrue(Questions.objects.filter(question_text='Rate your experience').exists())
 