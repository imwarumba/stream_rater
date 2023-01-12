from django.contrib import admin
from stream.models import Category, Streamer, UserProfile, Comment, SubComment

# Register your models here.


class StreamerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'name',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'date')
    exclude = ('streamer',)

class SubCommentAdmin(admin.ModelAdmin):
    list_display = ('father_comment', 'user_name', 'date')
    exclude = ('father_comment',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Streamer, StreamerAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubComment, SubCommentAdmin)
