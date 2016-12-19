from django import forms
from django.contrib import admin

from .models import Post

class PostAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
