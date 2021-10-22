from django.shortcuts import render
from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark


# Create your views here.
class BookmarkLV(ListView):
    model = Bookmark
    #디폴트 컨텍스트변수 object_list
    #모델명 (소문자)_list.html

class BookmarkDV(DetailView):
    model = Bookmark
    #디폴트 컨텍스트변수 object
    #모델명 (소문자)_list.html
