# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models


class Todo(models.Model):
    status_choice = (("N", "None"),
                     ("A", "Active"),
                     ("D", "Done"),)

    name = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=40)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=status_choice, blank=False, null=False, default="A")
    created = models.DateTimeField(blank=False, null=False)
    edited = models.DateTimeField(blank=False, null=False)
    due = models.DateTimeField(blank=False, null=False)
    reminder = models.IntegerField()
    flags = models.JSONField()

    def __str__(self):
        return self.name
