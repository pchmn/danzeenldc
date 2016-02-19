from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_user$', views.CreateUser.as_view(), name="create_user"),
    url(r'^login', views.login_user, name="login"),
    url(r'^logout$', views.logout_user, name="logout"),
    url(r'^profile/(?P<username>.*)$', views.get_profile, name="get_profile"),
    url(r'^change_password$', views.change_password, name="change_password")
]