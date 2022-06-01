from django.urls import re_path, path
from betogether.views import user, learnerProject, groupProject, wishList
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path(r"^user$", user, name="user"),
    re_path(r"^user/([0-9]+)$", user, name="user"),
    re_path(r"^project$", learnerProject, name="learner Project"),
    re_path(r"^project/([0-9]+)$", learnerProject, name="learner Project"),
    path("login", obtain_auth_token, name="auth-token"),
    re_path(r"^groupproject$", groupProject, name="group Project"),
    re_path(r"^wishlist$", wishList, name="wish list"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)