from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    register_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Active")

    # Custom related name for groups field
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        related_query_name="custom_user"
    )

    # Custom related name for user_permissions field
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users",
        related_query_name="custom_user"
    )

    def __str__(self):
        return self.username
    
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
