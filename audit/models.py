from django.db import models

class LogModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_string = models.TextField(blank=True, null=True)
    remote_addr = models.GenericIPAddressField(null=True)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"
