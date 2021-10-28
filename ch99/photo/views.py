from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from mysite.views import OwnerOnlyMixin
from photo.forms import PhotoInlineFormSet
from photo.models import Album, Photo

class AlbumLV(ListView):
    model = Album

class AlbumDV(DetailView):
    model = Album

class PhotoDV(DetailView):
    model = Photo



class PhotoCV(LoginRequiredMixin, CreateView):
    model = Photo
    fields= ('album','title','image','description')
    success_url = reverse_lazy('photo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PhotoChangeUV(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)


class PhotoUV(OwnerOnlyMixin, UpdateView):
    model = Photo
    fields= ('album','title','image','description')
    success_url = reverse_lazy('photo:index')

class PhotoDelV(OwnerOnlyMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')




class AlbumphotoCV(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

class AlbumDelV(OwnerOnlyMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('photo:index')


class AlbumChangeLV(LoginRequiredMixin, CreateView):
    model = Album
    fields= ('name','description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        #장고에 있는 디폴트 컨텍스트 변수 외에 추가적인 컨텍스트 변수를 정의하려고 하는 것
        context = super().get_context_data(**kwargs)(self)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FIELS)
        else:
            context['formset'] = PhotoInlineFormSet()
        return context

    def form_valid(self, form):
        form.isinstance.owner = self.request.user
        context = self.get_context_data
        formset = context['formset']

        for photoform in formset:
            photoform.isinstance.owner = self.request.user
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    

class AlbumPhotoUV(OwnerOnlyMixin, UpdateView):
    model = Album
    fields= ('name','description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        #장고에 있는 디폴트 컨텍스트 변수 외에 추가적인 컨텍스트 변수를 정의하려고 하는 것
        context = super().get_context_data(**kwargs)(self)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FIELS, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))