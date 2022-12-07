from django.db import models

from app_API.Users.User import People


class Group(models.Model):
    name = models.CharField(max_length=150)
    # leader = models.ForeignKey(People, on_delete=models.CASCADE, related_name="leader")
    leader = models.ManyToManyField(People, related_name="leader")
    members = models.ManyToManyField(People, through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"New_Member : {self.people.first_name} , In Group : {self.group.name}"


class RequestGroup(models.Model):
    sender = models.ForeignKey(People, on_delete=models.CASCADE)
    receiverGroup = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender : {self.sender.first_name}, Receiver Group : {self.receiverGroup.name}"
