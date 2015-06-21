from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.CampaignListView.as_view(), name='campaign_list'),
    url(r'^campaign/(?P<pk>\d+)/$', views.CampaignDetailView.as_view(), name='campaign_detail'),
    url(r'^MP/(?P<pk>\d+)/$', views.MPDetailView.as_view(), name='MP_detail'),
]
