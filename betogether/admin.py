from django.contrib import admin
from betogether.models import LearnerProject, User

# Register your models here.
admin.site.register(User)
admin.site.register(LearnerProject)