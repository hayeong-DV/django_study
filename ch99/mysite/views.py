from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
#뷰 처리 진입단계에서 적절한 권한을 갖추었는지 판별할때 사용하는 믹스인 클래스

class HomeView(TemplateView):
    template_name = 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

class OwnerOnlyMixin(AccessMixin):
    #로그인한 사용자가 콘텐츠 소유자인지 판별
    raise_exception = True
    #소유자가 아닌경우 True)>403처리>우리가 할 거
    #False면 로그인페이지로 리다이렉트
    permission_denied_message = 'owner on;y update/delete the object'
    #403시, 보여줄 메세지

def dispatch(self,request, *args, **kwargs):
    #get이전에 dispatch메소드오버라이딩
    #accessMixin 쓰는 경우엔 dispatch메소드오버라이딩 하는게 일반적
    obj = self.get_object()
    if request.user != obj.owner:
        return self.handle_no_permission()
    return super().dispatch(request, *args, **kwargs)