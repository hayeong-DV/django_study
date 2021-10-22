from django.contrib import admin

# Register your models here.
from bookmark.models import Bookmark

# @admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','title','url')

#데코레이터 안쓴다면
admin.site.register(Bookmark, BookmarkAdmin)