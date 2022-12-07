from django.db import models
from app_API.Groups.Group import Group
from app_API.Users.User import People


class Resource(models.Model):
    id_user = models.IntegerField(blank=True, default="1")
    name = models.CharField(max_length=150)
    year = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    pantone_value = models.CharField(max_length=100)
    url = models.URLField()
    text = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def res(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "color": self.color,
            "pantone_value": self.pantone_value,
            "id_user": self.id_user
        }

    def supports(self):
        return {
            "url": self.url,
            "text": self.text,

        }


class Like(models.Model):
    user = models.ForeignKey(People, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"User:{self.user.first_name} like {self.resource.name}"


class Comment(models.Model):
    user = models.ForeignKey(People, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    comments = models.TextField(max_length=1500)

    def __str__(self):
        return f"User:{self.user.first_name} like {self.resource.name}"
