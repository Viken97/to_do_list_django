from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ToDoList

class MainViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a test ToDoList and associate it with the user
        self.todo_list = ToDoList.objects.create(name='Test List', user=self.user)

    def test_index_view_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Test GET request
        response = self.client.get(reverse('index', args=[self.todo_list.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test List')
        self.assertTemplateUsed(response, 'main/list.html')

        # Test POST request
        response = self.client.post(reverse('index', args=[self.todo_list.id]), {'new': 'New Item'})
        self.assertEqual(response.status_code, 200)  

    def test_index_view_non_authenticated_user(self):
        # Simulate a non-authenticated user (not logging in)

        # Test GET request
        response = self.client.get(reverse('index', args=[self.todo_list.id]))
        self.assertEqual(response.status_code, 302)  

        # Test POST request
        response = self.client.post(reverse('index', args=[self.todo_list.id]), {'new': 'New Item'})
        self.assertEqual(response.status_code, 302)  

    def test_create_view_non_authenticated_user(self):
        # Simulate a non-authenticated user (not logging in)

        # Test GET request
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200) 

        self.assertTemplateUsed(response, 'main/create.html')
        self.assertContains(response, 'You need to be logged in to create a new list.')
    
    # def test_delete_list_on_view(self):
    #     # Simulate a non-authenticated user (not logging in)
        
    #     self.client.login(username='testuser', password='testpass')

    #     # Test GET request
    #     response = self.client.get(reverse('create'))
    #     self.assertEqual(response.status_code, 200) 

    #     self.assertTemplateUsed(response, 'main/create.html')
    #     self.assertContains(response, 'You need to be logged in to create a new list.')

        
    def test_view_non_authenticated_user(self):
        # Simulate a non-authenticated user (not logging in)

        # Test GET request
        response = self.client.get(reverse('view'))
        
        self.assertEqual(response.status_code, 200) 

        self.assertTemplateUsed(response, 'main/view.html')
        self.assertContains(response, 'You need to be logged in to view your lists.')
