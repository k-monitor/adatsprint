from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.LandingView.as_view(), name='landing'),

    url(r'^process/$', views.ProcessLandingView.as_view(), name='process_landing'),
    url(r'^process/dispatch/$', views.ProcessDispatch.as_view(), name='process_dispatch'),
    url(r'^process/(?P<pk>\d+)/claim/$', views.ClaimProcessView.as_view(), name='process_claim'),
    url(r'^process/(?P<pk>\d+)/$', views.ProcessView.as_view(), name='process'),
    url(r'^process/pending/$', views.PendingProcessListView.as_view(), name='process_pending'),

    url(r'^verify/$', views.VerifyLandingView.as_view(), name='verify_landing'),
    url(r'^verify/dispatch/$', views.VerifyDispatch.as_view(), name='verify_dispatch'),
    url(r'^verify/(?P<pk>\d+)/claim/$', views.ClaimVerifyView.as_view(), name='verify_claim'),
    url(r'^verify/(?P<pk>\d+)/$', views.VerifyView.as_view(), name='verify'),
    url(r'^verify/pending/$', views.PendingVerifyListView.as_view(), name='verify_pending'),
]
