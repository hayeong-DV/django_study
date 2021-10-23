from django.urls import path, re_path
from bookmark.views import *
from bookmark.models import Bookmark
app_name='bookmark'

urlpatterns=[
    path('', BookmarkLV.as_view(), name='index'),
    path('<int:pk>/', BookmarkDV.as_view(), name='detail'),
    path('add/', BookmarkCreateView.as_view(), name='add'),
    path('change/', BookmarkChangeView.as_view(), name='change'),
    path('<int:pk>/update/', BookmarkUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BookmarkDeleteView.as_view(), name='delete'),

]