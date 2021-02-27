from django.contrib import admin
from .models import LikesList, User, Posts, Profile, FollowingList, FollowerList

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Profile)
admin.site.register(FollowingList)
admin.site.register(FollowerList)
admin.site.register(LikesList)