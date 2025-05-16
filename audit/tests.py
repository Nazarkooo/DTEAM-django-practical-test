from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LogModel


class RequestLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_request_logging_basic(self):
        response = self.client.get(reverse('main_api:cvs-list'))
        
        self.assertEqual(LogModel.objects.count(), 1)
        
        log = LogModel.objects.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/api/cvs/')

    def test_logs_view_shows_latest_10(self):
        for i in range(15):
            LogModel.objects.create(
                method='GET',
                path=f'/test/{i}/',
                remote_addr='127.0.0.1'
            )
        
        response = self.client.get(reverse('audit:request_logs'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['logs']), 10)

    def test_logs_not_logged(self):
        response = self.client.get(reverse('audit:request_logs'))
        
        self.assertEqual(LogModel.objects.count(), 0)
