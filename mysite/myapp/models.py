from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField(default=0.0)
        
    def __str__(self):
        return self.title
