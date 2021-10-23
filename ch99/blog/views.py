from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from blog.models import Post
from django.conf import settings
# Create your views here.

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name='posts'
    paginate_by=2

class PostDV(DetailView):
    model=Post

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post={self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context


class PostAV(ArchiveIndexView):
    model=Post
    template_name = 'blog/post_archive.html' 
    date_field = 'modify_dt' 
    

class PostYAV(YearArchiveView):
    model=Post
    date_field = 'modify_dt'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model=Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model=Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model=Post
    date_field = 'modify_dt'

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.hmtl'

class TagObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(tags__name = self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


class SearchFormView(FormView):
    #FormView는 Get일때 폼을 화면에 보여주고, 입력기다림
    #데이터 입력>제출 시, Post로 접수> 데이터 유효성 검사>form_valid()실행후>리다이렉트
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        #유효성 검사 실시해 에러없음 form_valid실행
        #유효성 검사 통과하면 입력 데이터들은 cleaned_data 사전에 존재 
        searchWord = form.cleaned_data['search_word']
        #Q = filter조건 다양하게 가능
        #__incontains : 대소문자 구별x , 단어 포함되있는지
        #distinct: 중복 객체 제외
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | 
            Q(description__icontains=searchWord) |  Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_form'] = searchWord
        context['object_list'] = post_list

        #form_valid는 보통 HttpResponseRedirect객체 반환
        #지금건 재정의한거
        return render(self.request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title','slug', 'description', 'content','tags']
    initial={'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields=['title','slug', 'description', 'content','tags']
    success_url = reverse_lazy('blog:index')

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

