from django.urls import path, re_path
from bookmark.views import BookmarkLV, BookmarkDV
from bookmark.models import Bookmark
app_name='bookmark'

urlpatterns=[
    path('bookmark/', BookmarkLV.as_view(), name='index'),
    path('bookmark/<int:pk>/', BookmarkDV.as_view(), name='detail'),
]