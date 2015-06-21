from django.views import generic

from .models import Campaign, MP


class CampaignListView(generic.ListView):
    model = Campaign
    template_name = 'campaigns/campaign_list.html'


class CampaignDetailView(generic.DetailView):
    model = Campaign
    template_name = 'campaigns/campaign_detail.html'


class MPDetailView(generic.DetailView):
    model = MP
    template_name = 'campaigns/MP_detail.html'
