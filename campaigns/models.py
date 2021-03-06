from django.db import models
from django.db.models import Sum
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
    agreement_number = models.CharField(_("agreement number"), max_length=200, blank=True, null=True)
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
        permissions = (
            ('can_verify', _("Can verify MP")),
        )

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

    @property
    def is_processed(self):
        return self.status >= self.STATUS.PROCESSED

    @property
    def total_claimed_amount(self):
        return self.expense_set.exclude(claimed_amount=None).aggregate(Sum('claimed_amount'))

    @property
    def is_claimed_amount_consistent(self):
        return self.total == self.total_claimed_amount

    @property
    def process_duration(self):
        start = self.events.get_last_action(MPEvent.ACTION.PROCESS_START)
        stop = self.events.get_last_action(MPEvent.ACTION.PROCESS_DONE)

        if start is None or stop is None:
            return None

        assert stop.happened_on >= start.happened_on
        return stop.happened_on - start.happened_on

    @property
    def process_user(self):
        event_done = self.events.get_last_action(MPEvent.ACTION.PROCESS_DONE)
        return event_done.user if event_done is not None else None

    @property
    def verify_duration(self):
        start = self.events.get_last_action(MPEvent.ACTION.VERIFY_START)
        stop = self.events.get_last_action(MPEvent.ACTION.VERIFY_DONE)

        if start is None or stop is None:
            return None

        assert stop.happened_on >= start.happened_on
        return stop.happened_on - start.happened_on

    @property
    def verify_user(self):
        event_done = self.events.get_last_action(MPEvent.ACTION.VERIFY_DONE)
        return event_done.user if event_done is not None else None

    def as_csv_tuple(self):
        """
        Return the object in a tuple form suitable for putting in a CSV file
        """
        return (
            self.pk,
            self.campaign.pk,
            self.campaign.name,
            self.name,
            self.agreement_number,
            self.campaign_start.isoformat() if self.campaign_start else '',
            self.campaign_end.isoformat() if self.campaign_end else '',
            self.total,
            self.signed_on.isoformat() if self.signed_on else '',
            self.comment,
            self._pdf_page_count,
            self.get_status_display(),
        )

    as_csv_tuple.header = (
        'ID',
        'campaign ID',
        'campaign name',
        'name',
        'agreement_number',
        'campaign_start',
        'campaign_end',
        'total',
        'signed_on',
        'comment',
        'PDF page count',
        'status',
    )


class MPEventQueryset(models.QuerySet):
    def get_last_action(self, action):
        return self.filter(action=action).order_by('-happened_on').first()


class MPEventManager(models.Manager.from_queryset(MPEventQueryset)):
    use_for_related_fields = True


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

    objects = MPEventManager()

    def as_csv_tuple(self):
        """
        Return the object in a tuple form suitable for putting in a CSV file
        """
        return (
            self.pk,
            self.MP.pk,
            self.MP.name,
            self.get_action_display(),
            self.user.username,
            self.happened_on.isoformat(),
        )

    as_csv_tuple.header = (
        'ID',
        'MP ID',
        'MP name',
        'event',
        'user',
        'date',
    )


class Expense(models.Model):
    MP = models.ForeignKey('MP', verbose_name=_("MP"))
    row_number = models.PositiveIntegerField(_("row number"))
    invoice_reference = models.TextField(_("invoice reference"), blank=True)
    invoice_issue_date = models.DateField(_("issue date"), blank=True, null=True)
    provider = models.TextField(_("provider"), blank=True)
    product = models.TextField(_("product"), blank=True)
    payment_date = models.DateField(_("payment date"), blank=True, null=True)
    purpose = models.TextField(_("purpose"), blank=True, null=True)
    net_amount = models.PositiveIntegerField(_("net amount"), blank=True, null=True)
    VAT_amount = models.PositiveIntegerField(_("VAT amount"), blank=True, null=True)
    gross_amount = models.PositiveIntegerField(_("gross amount"), blank=True, null=True)
    claimed_amount = models.PositiveIntegerField(_("claimed amount"), blank=True, null=True)
    rejected = models.BooleanField(_("Rejected by authority"), default=False)

    class Meta:
        verbose_name = _("expense")
        verbose_name_plural = _("expenses")

    def as_csv_tuple(self):
        """
        Return the object in a tuple form suitable for putting in a CSV file
        """
        return (
            self.pk,
            self.MP.pk,
            self.MP.name,
            self.row_number,
            self.invoice_reference,
            self.invoice_issue_date.isoformat() if self.invoice_issue_date else '',
            self.provider,
            self.product,
            self.payment_date.isoformat() if self.payment_date else '',
            self.purpose,
            self.net_amount,
            self.VAT_amount,
            self.gross_amount,
            self.claimed_amount,
        )

    as_csv_tuple.header = (
        'ID',
        'MP ID',
        'MP name',
        'row_number',
        'invoice_reference',
        'invoice_issue_date',
        'provider',
        'product',
        'payment_date',
        'purpose',
        'net_amount',
        'VAT_amount',
        'gross_amount',
        'claimed_amount',
    )
