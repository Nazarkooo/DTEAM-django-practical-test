from django.test import TestCase, Client
from django.urls import reverse
from .models import CVModel, SkillModel, ProjectModel, ContactModel
from rest_framework.test import APITestCase
from rest_framework import status


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


class CVAPITests(APITestCase):
    def setUp(self):
        self.cv_data = {
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Test bio",
            "skills": [
                {"skill": "Python"},
                {"skill": "Django"}
            ],
            "projects": [
                {
                    "project": "Test Project",
                    "description": "Test Description"
                }
            ],
            "contacts": [
                {
                    "contact": "john@example.com",
                    "type": "email"
                }
            ]
        }
        
        self.cv = CVModel.objects.create(
            first_name="Jane",
            last_name="Smith",
            bio="Existing bio"
        )
        self.skill = SkillModel.objects.create(cv=self.cv, skill="JavaScript")
        self.project = ProjectModel.objects.create(
            cv=self.cv,
            project="Existing Project",
            description="Existing Description"
        )
        self.contact = ContactModel.objects.create(
            cv=self.cv,
            contact="jane@example.com",
            type="email"
        )

    def test_create_cv(self):
        url = reverse('main_api:cvs-list')
        response = self.client.post(url, self.cv_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CVModel.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'John')
        
        cv = CVModel.objects.get(first_name='John')
        self.assertEqual(cv.skills.count(), 2)
        self.assertEqual(cv.projects.count(), 1)
        self.assertEqual(cv.contacts.count(), 1)

    def test_get_cv_list(self):
        url = reverse('main_api:cvs-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_cv_detail(self):
        url = reverse('main_api:cvs-detail', kwargs={'pk': self.cv.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(len(response.data['skills']), 1)
        self.assertEqual(len(response.data['projects']), 1)
        self.assertEqual(len(response.data['contacts']), 1)


    def test_update_cv(self):
        url = reverse('main_api:cvs-detail', kwargs={'pk': self.cv.pk})
        patch_data = {
            "first_name": "Jane Patched",
            "bio": "Patched bio"
        }
        
        response = self.client.patch(url, patch_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.first_name, 'Jane Patched')
        self.assertEqual(self.cv.bio, 'Patched bio')
        self.assertEqual(self.cv.last_name, 'Smith')

    def test_delete_cv(self):
        url = reverse('main_api:cvs-detail', kwargs={'pk': self.cv.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CVModel.objects.count(), 0)
        self.assertEqual(SkillModel.objects.count(), 0)
        self.assertEqual(ProjectModel.objects.count(), 0)
        self.assertEqual(ContactModel.objects.count(), 0)

    def test_create_cv_invalid_data(self):
        url = reverse('main_api:cvs-list')
        invalid_data = {
            "first_name": "",
            "last_name": "Doe",
            "bio": "Test bio"
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_cv(self):
        url = reverse('main_api:cvs-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)