from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Employee, Notice, NoticeStatus, Forms, Questions, FormAssignedByTo
from django.utils import timezone
from .models import Manager  
from users.models import Users 

User = get_user_model()  # Use custom user model

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', pid='123456', password='password')
        self.client.login(username='testuser', password='password')
        
        # Create associated Employee model for user
        self.employee = Employee.objects.create(user=self.user, empname="Test Employee")

    def test_index_view(self):
        url = reverse('home:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_logout_link_view(self):
        url = reverse('home:logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users:login'))

    def test_user_profile_view(self):
        url = reverse('home:userProfile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/profile.html')

    def test_edit_profile_view(self):
        url = reverse('home:edit_profile')
        data = {'username': 'newusername', 'email': 'newemail@example.com'}
        response = self.client.post(url, data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertRedirects(response, reverse('home:userProfile'))
 

    def test_notice_view(self):
        url = reverse('home:notice')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/notice.html')

    def test_add_notice_view(self):
        url = reverse('home:add_notice')
        # Ensure the user has manager privileges
        self.employee.is_manager = True
        self.employee.save()
        data = {'title': 'Test Notice', 'content': 'This is a test notice.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Assuming redirect to 'home:notice'

    def test_employee_notices_view(self):
        url = reverse('home:employee_notices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/employee_notices.html')

    def test_acknowledge_notice_view(self):
        notice = Notice.objects.create(title="Test Notice", content="Notice content", posted_by=self.user)
        notice_status = NoticeStatus.objects.create(notice=notice, employee=self.employee, acknowledged=False)
        url = reverse('home:acknowledge_notice', args=[notice_status.id])
        response = self.client.post(url)
        notice_status.refresh_from_db()
        self.assertTrue(notice_status.acknowledged)
        self.assertRedirects(response, reverse('home:employee_notices'))

    def test_view_forms_view(self):
        url = reverse('home:view_forms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/view_forms.html')

    def test_assigned_forms_view(self):
        url = reverse('home:assigned_forms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/assigned_forms.html')


    def test_fill_feedback_form_view(self):
        # Create a Users instance first
        user = Users.objects.create(username='test_user', email='test@example.com', pid='200001')
        
        # Now create the Manager instance using the created Users instance
        manager = Manager.objects.create(user=user)  # Only pass the user

        form = Forms.objects.create(title="Test Form", created_by=user)  # Assuming created_by is a Users instance
        FormAssignedByTo.objects.create(form=form, employee=self.employee, manager=manager, assign_date=timezone.now())
        
        url = reverse('home:fill_feedback_form', args=[form.form_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/fill_feedback_form.html')


    def test_filled_forms_view(self):
        url = reverse('home:filled_forms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/filled_forms.html')

