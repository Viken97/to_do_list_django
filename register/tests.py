from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm

class RegisterViewTestCase(TestCase):
    def test_register_view_with_valid_data(self):
        # Prepare valid registration data
        valid_data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        }

        # Test POST request with valid data
        response = self.client.post(reverse('register'), valid_data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_with_different_passwords(self):
        # Prepare invalid registration data
        invalid_data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'TestPass123',
            'password2': 'DifferentPass',
        }

        # Test POST request with invalid data
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Registration failed, form is shown again
        self.assertTemplateUsed(response, 'register/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertContains(response, 'The two password fields didn’t match.')
 
    def test_register_view_without_email(self):
        # Prepare invalid registration data
        invalid_data = {
            'username': 'testuser',
            'email': '',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        }

        # Test POST request with invalid data
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Registration failed, form is shown again
        self.assertTemplateUsed(response, 'register/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertContains(response, 'This field is required.')
    
    def test_register_view_with_weak_password(self):
        # Prepare invalid registration data
        invalid_data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': '123',
            'password2': '123',
        }

        # Test POST request with invalid data
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Registration failed, form is shown again
        self.assertTemplateUsed(response, 'register/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertContains(response, 'Your password must contain at least 8 characters.')



