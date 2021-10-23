from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from photo.models import Album, Photo

class AlbumLV(ListView):
    model = Album

class AlbumDV(DetailView):
    model = Album

class PhotoDV(DetailView):
    model = Photo

