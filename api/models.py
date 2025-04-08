from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class DailyStudy(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='months')
    date = models.DateField(null=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("Date cannot be in the past.")

    
