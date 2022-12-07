from django.urls import path

from . import viewsUser

urlpatterns = [
    path('createUsers', viewsUser.createUsers, name='users'),
    path('users/list', viewsUser.listUsers, name='listUsers'),
    path('updateUSer', viewsUser.updateUSer, name='updateUSer'),
    path('deleteUser', viewsUser.deleteUser, name='deleteUser'),
    path('users/<str:ID>', viewsUser.userID, name='userID'),
    path('register', viewsUser.register, name='register'),
    path('login', viewsUser.login, name='login'),
    path('sendPeople', viewsUser.sendPeople, name='sendPeople'),

]
