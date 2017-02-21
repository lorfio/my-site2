from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.log_in, name='log_in'),
	url(r'^logout/$', views.log_out, name='log_out'),
	url(r'^registration/$', views.registration, name='registration'),
	url(r'^user-profile/(?P<pk>[0-9]+)/$', views.userProfile, name='userProfile'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]
