from django.db import models

from app_API.Users.User import People
from django.contrib.auth.models import User


class Friend(models.Model):
    users1 = models.ManyToManyField(People)
    current_user = models.ForeignKey(People, related_name='owner', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Sender: {self.current_user}"

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender = models.ForeignKey(People, null=True, related_name='sender1', on_delete=models.CASCADE)
    receiver = models.ForeignKey(People, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender: {self.sender.first_name} , Receiver: {self.receiver.first_name}"
