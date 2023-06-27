from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('sports', 'Sports'),
        ('cooking', 'Cooking'),
        ('technology', 'Technology'),
        ('life style', 'Life style'),
        ('car', 'Car')
    )
    title = models.CharField(max_length=300)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='life style')
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.title
