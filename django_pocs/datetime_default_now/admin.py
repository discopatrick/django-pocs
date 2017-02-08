from django import forms
from django.contrib import admin

from .models import Post, PostWithDefaultDateTime, PostWithCleanMethod

class PostAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

class PostWithDefaultDateTimeAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = PostWithDefaultDateTime

@admin.register(PostWithDefaultDateTime)
class PostAdmin(admin.ModelAdmin):
    form = PostWithDefaultDateTimeAdminForm

class PostWithCleanMethodAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = PostWithCleanMethod

@admin.register(PostWithCleanMethod)
class PostAdmin(admin.ModelAdmin):
    form = PostWithCleanMethodAdminForm
