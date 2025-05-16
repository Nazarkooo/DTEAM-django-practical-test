from django.test import TestCase, Client
from django.urls import reverse
from .models import CVModel, SkillModel, ProjectModel, ContactModel


class CVViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cv = CVModel.objects.create(
            first_name="Test",
            last_name="User",
            bio="Test bio"
        )
        self.skill = SkillModel.objects.create(
            skill="Python",
            cv=self.cv
        )
        self.project = ProjectModel.objects.create(
            project="Test Project",
            description="Test description",
            cv=self.cv
        )
        self.contact = ContactModel.objects.create(
            contact="test@example.com",
            type="email",
            cv=self.cv
        )

    def test_cv_list_view(self):
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cv_list.html')
        self.assertContains(response, "Test User")
        self.assertContains(response, "Python")

    def test_cv_detail_view(self):
        response = self.client.get(reverse('main:cv_detail', args=[self.cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cv_detail.html')
        self.assertContains(response, "Test User")
        self.assertContains(response, "Python")
        self.assertContains(response, "Test Project")
        self.assertContains(response, "test@example.com")
