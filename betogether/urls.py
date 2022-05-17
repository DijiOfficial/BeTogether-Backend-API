from django.urls import re_path
from betogether.views import user

urlpatterns = [
    re_path(r"^user$", user, name="user"),
    re_path(r"^user/([0-9]+)$", user, name="user"),
]