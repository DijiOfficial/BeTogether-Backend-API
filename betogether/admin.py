from django.contrib import admin
from betogether.models import LearnerProject, User, groupProject

# Register your models here.
admin.site.register(User)
admin.site.register(groupProject)
admin.site.register(LearnerProject)