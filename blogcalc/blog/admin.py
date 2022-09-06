from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Blogger, Blog_post

# Register your models here.

class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (BloggerInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class Blog_postAdmin(admin.ModelAdmin):
    list_display = ("title", "blogger", "date_of_origin", "date_of_update", "dislikes", )
    list_filter = ("blogger", "date_of_origin", )

admin.site.register(Blog_post, Blog_postAdmin)