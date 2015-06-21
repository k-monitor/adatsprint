from operator import attrgetter

from django.test import TestCase

from .models import Campaign, MP


class CampaignTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.campaign = Campaign.objects.create(name='Baptiste 2015')

    def test_custom_manager(self):
        MP.objects.create(campaign=self.campaign, name='unfinished/verified', finished=False, verified=True)
        MP.objects.create(campaign=self.campaign, name='finished/unverified', finished=True, verified=False)

        self.assertQuerysetEqual(MP.objects.finished(), ['finished/unverified'], attrgetter('name'))
        self.assertQuerysetEqual(MP.objects.unfinished(), ['unfinished/verified'], attrgetter('name'))
        self.assertQuerysetEqual(MP.objects.verified(), ['unfinished/verified'], attrgetter('name'))
        self.assertQuerysetEqual(MP.objects.unverified(), ['finished/unverified'], attrgetter('name'))

    def test_completion_rate_empty_campaign(self):
        self.assertAlmostEqual(self.campaign.completion_rate, 1)

    def test_completion_rate(self):
        MP.objects.create(campaign=self.campaign, name='unfinished', finished=False)
        self.assertAlmostEqual(self.campaign.completion_rate, 0)
        MP.objects.create(campaign=self.campaign, name='unfinished', finished=True)
        self.assertAlmostEqual(self.campaign.completion_rate, 0.5)

    def test_verification_rate_empty_campaign(self):
        self.assertAlmostEqual(self.campaign.verification_rate, 1)

    def test_verification_rate(self):
        MP.objects.create(campaign=self.campaign, name='unfinished', verified=False)
        self.assertAlmostEqual(self.campaign.verification_rate, 0)
        MP.objects.create(campaign=self.campaign, name='unfinished', verified=True)
        self.assertAlmostEqual(self.campaign.verification_rate, 0.5)
