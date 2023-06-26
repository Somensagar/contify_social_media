from django.contrib import admin
from .models import UserProfile, Post, Friend


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Friend)