from operator import attrgetter

from django.test import TestCase

from .models import Campaign, MP


class CampaignTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.campaign = Campaign.objects.create(name='Baptiste 2015')

    def test_custom_manager(self):
        status = [
            (MP.STATUS.UNPROCESSED, "unprocessed"),
            (MP.STATUS.PROCESSING, "processing"),
            (MP.STATUS.PROCESSED, "processed"),
            (MP.STATUS.VERIFYING, "verifying"),
            (MP.STATUS.VERIFIED, "verified"),
        ]
        for status_name, status_value in status:
            MP.objects.create(campaign=self.campaign, name=status_name, status=status_value)

        for status_name, status_value in status:
            custom_manager_method = getattr(MP.objects, status_name)
            queryset = custom_manager_method()
            self.assertQuerysetEqual(queryset, [status_name], attrgetter('name'))

    def test_completion_rate_empty_campaign(self):
        self.assertAlmostEqual(self.campaign.completion_rate, 1)

    def test_completion_rate(self):
        MP.objects.create(campaign=self.campaign, name='unfinished', status=MP.STATUS.EMPTY)
        self.assertAlmostEqual(self.campaign.completion_rate, 0)
        MP.objects.create(campaign=self.campaign, name='unfinished', status=PROCESSED)
        self.assertAlmostEqual(self.campaign.completion_rate, 0.5)

    def test_verification_rate_empty_campaign(self):
        self.assertAlmostEqual(self.campaign.verification_rate, 1)

    def test_verification_rate(self):
        MP.objects.create(campaign=self.campaign, name='unfinished', status=PROCESSED)
        self.assertAlmostEqual(self.campaign.verification_rate, 0)
        MP.objects.create(campaign=self.campaign, name='unfinished', status=VERIFIED)
        self.assertAlmostEqual(self.campaign.verification_rate, 0.5)
