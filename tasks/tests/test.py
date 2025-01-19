from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from tasks.models import Task
from django.forms.models import model_to_dict
import json

from tasks.serializers import TaskSerializer


class TaskTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('task_list_create')
        self.mock_task_data: dict = {
            'title': 'test title',
            'description': 'test description',
            'posted': True
        }
        self.task = Task.objects.create(
            **self.mock_task_data
        )
        self.url_with_id = f'{self.base_url}1'

    def test_status_code_get_task(self):
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_list_task_content(self):
        response = self.client.get(
            self.base_url
        )
        response = response.json()
        """
        Deve retornar 1, pois no SetUp estou criando uma Task.
        """
        self.assertEqual(
            len(response),
            1
        )
       
    def test_status_code_post_task(self):
        response = self.client.post(
            self.base_url,
            data=self.mock_task_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_status_code_get_one_task(self):
        # Nota: Uma instância de `Task` já foi criada no método `setUp`.
        response = self.client.get(self.url_with_id)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_get_one_task(self):
        response = self.client.get(self.url_with_id)
        response_data = response.json()
        expected_data = TaskSerializer(self.task).data
        print(response_data)
        self.assertEqual(
            response_data,
            expected_data
        )
    
    def test_status_code_delete_task(self):
        response = self.client.delete(
            self.url_with_id
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_update_task_status_code(self):
        new_data = {
            'title': 'task-updated',
            'description': '',
            'posted': False
        }
        response = self.client.put(
            self.url_with_id,
            data=new_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_task_title(self):
        new_data = {
            'title': 'task-updated',
            'description': '',
            'posted': False
        }
        response = self.client.put(
            self.url_with_id,
            data=new_data
        )
        json_response = response.json()
        self.assertEqual(
            json_response['title'],
            new_data['title']
        )
