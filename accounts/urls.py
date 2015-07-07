from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, kwargs={'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
