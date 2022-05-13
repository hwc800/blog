
from django.conf.urls import url

from box import views


urlpatterns = [
    url(r'^comment', views.comment, name='comment'),
    url(r'^about', views.about, name='about'),
    url(r'^box_content', views.box_content, name='box_content'),
    url(r'^box_mode', views.box_mode, name='box_mode'),
    url(r'^box_index', views.box_index, name='box_index'),
    url(r'^box_show_mode', views.box_show_mode, name='box_show_mode'),
    url(r'^user_index', views.user_index, name='user_index'),
    url(r'^login', views.login, name='login'),
    url(r'^set_token', views.set_token, name='set_token'),
    url(r'^', views.box_index),
]