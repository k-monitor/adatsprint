from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .utils import get_pdf_page_count

class Campaign(models.Model):
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now=True)

    @property
    def completion_rate(self):
        total = self.participants.count()
        completed = self.participants.completed().count()

        if not total:
            return 1

        return completed / total

    @property
    def verification_rate(self):
        total = self.participants.count()
        verified = self.participants.verified().count()

        if not total:
            return 1

        return verified / total

    class Meta:
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")

    def __str__(self):
        return self.name


class MPQuerySet(models.QuerySet):
    def unprocessed(self):
        return self.filter(status=self.model.STATUS.UNPROCESSED)

    def processing(self):
        return self.filter(status=self.model.STATUS.PROCESSING)

    def processed(self):
        return self.filter(status=self.model.STATUS.PROCESSED)

    def verifying(self):
        return self.filter(status=self.model.STATUS.VERIFYING)

    def verified(self):
        return self.filter(status=self.model.STATUS.VERIFIED)

    def completed(self):
        return self.filter(status__gte=self.model.STATUS.PROCESSED)


class MP(models.Model):
    class STATUS:
        UNPROCESSED = 1
        PROCESSING = 2
        PROCESSED = 3
        VERIFYING = 4
        VERIFIED = 5

        choices = [
            (UNPROCESSED, _("unprocessed")),
            (PROCESSING, _("processing")),
            (PROCESSED, _("processed")),
            (VERIFYING, _("verifying")),
            (VERIFIED, _("verified")),
        ]

    campaign = models.ForeignKey('Campaign', verbose_name=_("campaign"), related_name='participants')
    name = models.CharField(_("name"), max_length=200)
    agreement_number = models.CharField(_("agreement number"), max_length=50, blank=True, null=True)
    campaign_start = models.DateField(_("campaign start"), blank=True, null=True)
    campaign_end = models.DateField(_("campaign end"), blank=True, null=True)
    total = models.PositiveIntegerField(_("total"), blank=True, null=True)
    signed_on = models.DateField(_("signed on"), blank=True, null=True)
    comment = models.TextField(_("comment"), blank=True)

    pdf_file = models.FileField(_("PDF file"), blank=True)
    _pdf_page_count = models.PositiveIntegerField(_("PDF page count"), blank=True, null=True, editable=False)

    status = models.PositiveIntegerField(_("status"), choices=STATUS.choices, default=STATUS.UNPROCESSED)

    processed_by = models.ForeignKey('auth.User', verbose_name=_("processed by"), related_name='+', blank=True, null=True)
    verified_by = models.ForeignKey('auth.User', verbose_name=_("verified by"), related_name='+', blank=True, null=True)

    objects = MPQuerySet.as_manager()

    class Meta:
        verbose_name = _("MP")
        verbose_name_plural = _("MPs")

    def __str__(self):
        return self.name

    @property
    def pdf_page_count(self):
        """
        Return the number of pages in the PDF.
        That number is calculated on the fly on first access and stored for later.
        """
        if self._pdf_page_count is None:
            self._pdf_page_count = get_pdf_page_count(self.pdf_file)
            self.save()
        return self._pdf_page_count


class MPEvent(models.Model):
    class ACTION:
        INSERTED = 'inserted'
        PROCESS_START = 'process start'
        PROCESS_DONE = 'process done'
        VERIFY_START = 'verify start'
        VERIFY_DONE = 'verify done'

        PROCESS_UNCLAIM = 'process unclaim'
        VERIFY_UNCLAIM = 'verify unclaim'

        choices = [
            (INSERTED, _("inserted")),
            (PROCESS_START, _("process start")),
            (PROCESS_DONE, _("process done")),
            (VERIFY_START, _("verify start")),
            (VERIFY_DONE, _("verify done")),

            (PROCESS_UNCLAIM, _("process unclaim")),
            (VERIFY_UNCLAIM, _("verify unclaim")),
        ]

    MP = models.ForeignKey('MP', verbose_name=_("MP"), related_name='events')
    action = models.CharField(_("action"), max_length=50, choices=ACTION.choices)
    user = models.ForeignKey('auth.User', verbose_name=_("user"))
    happened_on = models.DateTimeField(_("happened on"), default=timezone.now)


class Expense(models.Model):
    MP = models.ForeignKey('MP', verbose_name=_("MP"))
    row_number = models.PositiveIntegerField(_("row number"))
    invoice_reference = models.CharField(_("invoice reference"), max_length=50, blank=True)
    invoice_issue_date = models.DateField(_("issue date"), blank=True, null=True)
    provider = models.CharField(_("provider"), max_length=200, blank=True)
    product = models.CharField(_("product"), max_length=200, blank=True)
    payment_date = models.DateField(_("payment date"), blank=True, null=True)
    purpose = models.CharField(_("purpose"), max_length=200, blank=True, null=True)
    net_amount = models.PositiveIntegerField(_("net amount"), blank=True, null=True)
    VAT_amount = models.PositiveIntegerField(_("VAT amount"), blank=True, null=True)
    gross_amount = models.PositiveIntegerField(_("gross amount"), blank=True, null=True)
    claimed_amount = models.PositiveIntegerField(_("claimed amount"), blank=True, null=True)

    class Meta:
        verbose_name = _("expense")
        verbose_name_plural = _("expenses")
