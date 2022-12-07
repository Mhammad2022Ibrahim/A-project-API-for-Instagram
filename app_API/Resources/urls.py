from django.urls import path

from . import viewsResource

urlpatterns = [
    path('unknown', viewsResource.resource, name='resource'),
    path('unknown/list', viewsResource.listunknown, name='listunknown'),
    path('unknown/<str:ID>', viewsResource.unknownID, name='unknownID'),
    path('sendResource', viewsResource.sendResource, name='sendResource'),
    path('add_like', viewsResource.add_like, name='add_like'),
    path('add_comment', viewsResource.add_comment, name='add_comment'),
    path('delete_comment', viewsResource.delete_comment, name='delete_comment'),
]
