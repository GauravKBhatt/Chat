from django.urls import path
from .views import *


urlpatterns = [
    path('create-room/<path:url>/<uuid:uuid>/<str:name>/', Room.as_view(), name='create-room'),
    path('chat-admin/<str:uuid>/',Room.as_view(),name='room'),
    path('chat-admin/',Admin.as_view(),name='admin'),
    path('chat-admin/add-user/<str:status>/',User.as_view(),name='add_edit_user'),
    path('chat-admin/users/<uuid:uuid>/',User.as_view(),name='user_detail'),
    # path('chat-admin/users/<uuid:uuid>/edit/',views.edit_user,name='edit_user'),
    path('chat-admin/delete-room/<str:uuid>/',Delete.as_view(),name='delete_room')]