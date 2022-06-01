from django.contrib import admin
from betogether.models import LearnerProject, User, GroupProject, Groups, UserPerGroup, WishList

# Register your models here.
admin.site.register(User)
admin.site.register(GroupProject)
admin.site.register(LearnerProject)
admin.site.register(Groups)
admin.site.register(UserPerGroup)
admin.site.register(WishList)