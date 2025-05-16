from django.db import models

class CVModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SkillModel(models.Model):
    skill = models.CharField(max_length=255)
    cv = models.ForeignKey(CVModel, related_name="skills", on_delete=models.CASCADE)

    def __str__(self):
        return self.skill

class ProjectModel(models.Model):
    project = models.CharField(max_length=255)
    description = models.TextField()
    cv = models.ForeignKey(CVModel, related_name="projects", on_delete=models.CASCADE)

    def __str__(self):
        return self.project

class ContactModel(models.Model):
    class ContactType(models.TextChoices):
        EMAIL = "email"
        PHONE = "phone"
        LINKEDIN = "linkedin"
        GITHUB = "github"
        OTHER = "other"
        
    contact = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ContactType.choices, default=ContactType.OTHER)
    cv = models.ForeignKey(CVModel, related_name="contacts", on_delete=models.CASCADE)

    def __str__(self):
        return self.contact
