from django.contrib import admin

# Register your models here.
from blog.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','modify_dt','tag_list')
    list_filter = ('modify_dt',)
    search_fields= ('title','content')
    prepopulated_fields = {'slug': ('title',)} 

    #post레코드 리스트를 가져옴
    #post와 tag테이블은 manytomany관계이니까>
    #tag테이블 관련 레코드 한번의 쿼리로 미리 가져오기 위함
    #N:N관계에서 쿼리 횟수를 줄여 성능 높이려면, prefecth_related()메소드 사용
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    #tag_list항목에 ㅂ여줄 내용 정의 
    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())