from django.contrib import admin
from photo.models import Album, Photo
# Register your models here.

#StackedInline: album, photo는 1:N관계
#앨범 보여줄 때 연결된 사진은 같이 보여줄 수 있음
#StackedInline(세로나열) or Tabularinline(테이블처럼 행으로 보여줌)사용해서
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2 #이미 존재하는 객체 외 추가로 입력가능한 photo테이블 객체수는 2

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines=(PhotoInline,) #앨범 객체 수정사항 보일때 PhotoInline클래스에서 정의한 사항 같이 보여줌
    list_display=('id','name','description')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display=('id','title','upload_dt')