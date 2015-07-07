import random

from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from .forms import MPProcessForm, MPVerifyForm, EXPENSE_FORMSET_FIELDS, EXPENSE_FORMSET_WDIGETS
from .models import Campaign, MP, MPEvent, Expense


class LandingView(generic.TemplateView):
    template_name = 'campaigns/landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context.update({
            'completed': MP.objects.completed().count(),
            'verified': MP.objects.verified().count(),
            'total': MP.objects.count(),
        })
        return context


class MPStatusMixin(object):
    """
    Filter get_queryset() so that it only includes objects that have the given
    status.
    """
    model = MP
    status = None

    def get_queryset(self):
        assert self.status is not None
        queryset = super(MPStatusMixin, self).get_queryset()
        queryset = queryset.filter(status=self.status)
        return queryset


class MPEventMixin(object):
    """
    A mixin that provides a record() method on the view.
    The method records an MPEvent with sensible defaults.
    """
    action = None  # Optional

    def record(self, **kwargs):
        if getattr(self, 'object', None) is not None:
            kwargs.setdefault('MP', self.object)

        if self.action is not None:
            kwargs.setdefault('action', self.action)

        kwargs.setdefault('user', self.request.user)

        return MPEvent.objects.create(**kwargs)

    def form_valid(self, form):
        response = super(MPEventMixin, self).form_valid(form)
        self.record()
        return response


class BaseDispatchView(MPStatusMixin, SingleObjectMixin, generic.RedirectView):
    """
    A view that picks a random MP with the given status (MPStatusMixin) and
    redirect to the `pattern_name` associated with that MP.
    """
    permanent = False

    def get_redirect_url(self):
        mp_list = self.get_queryset().values_list('pk', flat=True)
        mp_id = random.choice(mp_list)
        # TODO: handle empty queryset
        return super(BaseDispatchView, self).get_redirect_url(pk=mp_id)


class BaseClaimView(MPEventMixin, MPStatusMixin, SingleObjectMixin, generic.RedirectView):
    """
    Get an MP based on the pk provided in the URL.
    Update its status based on the view's attribute (set by child classes) and
    record the corresponding event.
    Finally, redirect to the view given by the `pattern_name` attribute.
    """
    status = None
    next_status = None
    action = None
    permanent = False

    def get_queryset(self):
        queryset = super(BaseClaimView, self).get_queryset()
        queryset = queryset.select_for_update()  # prevents race condition
        return queryset

    def get(self, request, *args, **kwargs):
        assert self.status is not None
        assert self.next_status is not None
        assert self.action is not None

        with transaction.atomic():
            self.object = self.get_object()
            self.object.status = self.next_status
            self.object.save()
            self.record()

        return super(BaseClaimView, self).get(request, *args, **kwargs)


class ProcessLandingView(MPStatusMixin, generic.ListView):
    """
    Display a list of MPs that need to be processed.
    """
    status = MP.STATUS.UNPROCESSED
    template_name = 'campaigns/process_landing.html'

    def get_queryset(self):
        queryset = super(ProcessLandingView, self).get_queryset()
        queryset = queryset.select_related('campaign')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcessLandingView, self).get_context_data(**kwargs)
        context.update({
            'total': MP.objects.count(),
            'completed': MP.objects.completed().count(),
        })
        return context


class ProcessDispatch(BaseDispatchView):
    status = MP.STATUS.UNPROCESSED
    pattern_name = 'campaigns:process_claim'


class ClaimProcessView(BaseClaimView):
    status = MP.STATUS.UNPROCESSED
    next_status = MP.STATUS.PROCESSING
    action = MPEvent.ACTION.PROCESS_START
    pattern_name = 'campaigns:process'


class ProcessView(MPEventMixin, MPStatusMixin, generic.UpdateView):
    status = MP.STATUS.PROCESSING
    action = MPEvent.ACTION.PROCESS_DONE
    form_class = MPProcessForm
    template_name = 'campaigns/process.html'

    def get_success_url(self):
        urls = {
            'DISPATCH': reverse('campaigns:process_dispatch'),
            'LANDING': reverse('campaigns:process_landing'),
        }
        action = self.request.POST.get('action')
        if action not in urls:
            action = 'LANDING'

        return urls[action]

    def form_valid(self, form):
        response = super(ProcessView, self).form_valid(form)
        self.record()
        return response


class PendingProcessListView(MPStatusMixin, generic.ListView):
    status = MP.STATUS.PROCESSING
    template_name = 'campaigns/process_pending.html'

    def get_queryset(self):
        queryset = super(PendingProcessListView, self).get_queryset()
        queryset = queryset.select_related('campaign')
        queryset = queryset.prefetch_related('events')  # TODO: select_related on event.user
        return queryset


class VerifyLandingView(MPStatusMixin, generic.ListView):
    """
    Display a list of MPs that need to be processed.
    """
    status = MP.STATUS.PROCESSED
    template_name = 'campaigns/verify_landing.html'

    def get_queryset(self):
        queryset = super(VerifyLandingView, self).get_queryset()
        queryset = queryset.select_related('campaign')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(VerifyLandingView, self).get_context_data(**kwargs)
        context.update({
            'total': MP.objects.count(),
            'verified': MP.objects.verified().count(),
        })
        return context


class VerifyDispatch(BaseDispatchView):
    status = MP.STATUS.PROCESSED
    pattern_name = 'campaigns:verify_claim'


class ClaimVerifyView(BaseClaimView):
    status = MP.STATUS.PROCESSED
    next_status = MP.STATUS.VERIFYING
    action = MPEvent.ACTION.VERIFY_START
    pattern_name = 'campaigns:verify'


class VerifyView(MPEventMixin, MPStatusMixin, generic.UpdateView):
    status = MP.STATUS.VERIFYING
    action = MPEvent.ACTION.VERIFY_DONE
    form_class = MPVerifyForm
    template_name = 'campaigns/verify.html'

    def get_success_url(self):
        urls = {
            'DISPATCH': reverse('campaigns:verify_dispatch'),
            'LANDING': reverse('campaigns:verify_landing'),
        }
        action = self.request.POST.get('action')
        if action not in urls:
            action = 'LANDING'

        return urls[action]

    def form_valid(self, form):
        response = super(VerifyView, self).form_valid(form)
        self.record()
        return response


class PendingVerifyListView(MPStatusMixin, generic.ListView):
    status = MP.STATUS.VERIFYING
    template_name = 'campaigns/verify_pending.html'
