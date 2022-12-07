from django.urls import path

from . import viewsFriend

urlpatterns = [
    path('sendRequest', viewsFriend.sendRequest, name='sendRequest'),
    path('delete_request', viewsFriend.delete_request, name='delete_request'),
    path('add_or_remove_friend', viewsFriend.add_or_remove_friend, name='add_or_remove_friend'),
    path('getResourceFriend', viewsFriend.getResourceFriend, name='getResourceFriend'),
]
