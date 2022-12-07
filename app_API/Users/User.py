from django.db import models

from django.contrib.auth.models import User


# Create your models here.

class People(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.URLField()
    job = models.CharField(max_length=100)
    createDate = models.DateTimeField(auto_now=True)
    url = models.URLField()
    text = models.TextField()
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    def datas(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
        }

    def supports(self):
        return {
            "url": self.url,
            "text": self.text
        }

    def create(self):
        return {
            "name": self.first_name,
            "job": self.job,
            "id": self.id,
            "createDate": self.createDate
        }

    def update(self):
        return {
            "name": self.first_name,
            "job": self.job,
            "updateDate": self.createDate
        }
