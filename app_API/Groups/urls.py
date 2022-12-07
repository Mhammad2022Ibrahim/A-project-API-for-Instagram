from django.urls import path

from . import viewsGroup

urlpatterns = [
    path('createGroup', viewsGroup.createGroup, name='createGroup'),
    path('groupRequest', viewsGroup.groupRequest, name='groupRequest'),
    path('delete_requestGroup', viewsGroup.delete_requestGroup, name='delete_requestGroup'),
    path('add_or_remove_member', viewsGroup.add_or_remove_member, name='add_or_remove_member'),
    path('createResource', viewsGroup.createResource, name='createResource'),
    path('getResourceMembers', viewsGroup.getResourceMembers, name='getResourceMembers'),
    path('getLeaderToMember', viewsGroup.getLeaderToMember, name='getLeaderToMember'),
    path('leftLeader', viewsGroup.leftLeader, name='leftLeader'),

]
