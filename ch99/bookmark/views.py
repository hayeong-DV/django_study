from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
#로그인 데코레이터 기능 클래스에 적용시 사용
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
#소유저만 콘텐츠 수정 가능하도록 하는 클래스 
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


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields=['title','url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookmarkChangeView(LoginRequiredMixin, ListView):
    template_name='bookmark/bookmark_change_list.html'

    def get_queryset(self):
        #화면에 출력할 레코드 리스트 반환
        return Bookmark.objects.filter(owner=self.request.user)


class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model = Bookmark
    fields=['title','url']
    success_url = reverse_lazy('bookmark:index')


class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')

