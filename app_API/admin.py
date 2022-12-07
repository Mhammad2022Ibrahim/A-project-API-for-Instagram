from django.contrib import admin

from app_API.Friends.Friend import Friend, FriendRequest
from app_API.Groups.Group import *
from app_API.Resources.Resource import Resource, Like, Comment
from app_API.Users.User import People

# Register your models here.
admin.site.register(People)
admin.site.register(Resource)
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(RequestGroup)
