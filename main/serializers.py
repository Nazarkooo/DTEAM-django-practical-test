
from rest_framework import serializers
from .models import CVModel, SkillModel, ProjectModel, ContactModel


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = ['id', 'skill']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ['id', 'project', 'description']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = ['id', 'contact', 'type']

class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)
    class Meta:
        model = CVModel
        fields = ['id', 'first_name', 'last_name', 'bio', 'skills', 'projects', 'contacts']

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        projects_data = validated_data.pop('projects', [])
        contacts_data = validated_data.pop('contacts', [])
        cv = CVModel.objects.create(**validated_data)
        for skill_data in skills_data:
            SkillModel.objects.create(cv=cv, **skill_data)
        for project_data in projects_data:
            ProjectModel.objects.create(cv=cv, **project_data)
        for contact_data in contacts_data:
            ContactModel.objects.create(cv=cv, **contact_data)
        return cv
