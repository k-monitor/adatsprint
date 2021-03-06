from django import forms
from django.forms.models import inlineformset_factory

from .models import MP, Expense


class BaseMPForm(forms.ModelForm):
    NEXT_STATUS = None
    USER_ATTR = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BaseMPForm, self).__init__(*args, **kwargs)

        ExpenseFormset = inlineformset_factory(MP, Expense, **self.get_formset_kwargs())
        self.expense_formset = ExpenseFormset(*args, **kwargs)

        for f in self.fields.values():
            widget = f.widget
            css_classes = set(widget.attrs.get('class', '').split())
            css_classes.add('form-control')
            widget.attrs['class'] = ' '.join(css_classes)

    def get_formset_kwargs(self):
        return {
            'fields': EXPENSE_FORMSET_FIELDS,
            'widgets': EXPENSE_FORMSET_WDIGETS,
            'can_delete': False,
        }

    def is_valid(self):
        form_valid = super(BaseMPForm, self).is_valid()
        formset_valid = self.expense_formset.is_valid()
        return form_valid and formset_valid

    def save(self, commit=True):
        assert commit  # commit=False is not supported
        instance = super(BaseMPForm, self).save(commit=False)
        instance.status = self.NEXT_STATUS
        if self.USER_ATTR is not None:
            setattr(instance, self.USER_ATTR, self.user)
        if commit:
            instance.save()
            self.expense_formset.save()

        return instance

    class Meta:
        model = MP
        fields = [
            'name',
            'agreement_number',
            'campaign_start',
            'campaign_end',
            'total',
            'signed_on',
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
            'campaign_start': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade'}),
            'campaign_end': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade'}),
            'signed_on': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade'}),
        }


class MPProcessForm(BaseMPForm):
    NEXT_STATUS = MP.STATUS.PROCESSED
    USER_ATTR = 'processed_by'

    def get_formset_kwargs(self):
        assert self.instance is not None
        kwargs = super(MPProcessForm, self).get_formset_kwargs()
        # One bonus form is added for javascript formset cloning purposes
        kwargs['extra'] = (self.instance.pdf_page_count or 1) * 8 + 1
        return kwargs


class MPVerifyForm(BaseMPForm):
    NEXT_STATUS = MP.STATUS.VERIFIED
    USER_ATTR = 'verified_by'

    def get_formset_kwargs(self):
        assert self.instance is not None
        kwargs = super(MPVerifyForm, self).get_formset_kwargs()
        # One bonus form is added for javascript formset cloning purposes
        kwargs['extra'] = 1
        return kwargs


EXPENSE_FORMSET_FIELDS = [
    'rejected',
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
]
EXPENSE_FORMSET_WDIGETS = {
    'row_number': forms.TextInput(attrs={'size': 2, 'class': 'form-control'}),
    'invoice_reference': forms.Textarea(attrs={'rows': 1, 'cols': 10, 'class': 'form-control enlarge-on-focus'}),
    'invoice_issue_date': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade', 'class': 'form-control'}),
    'provider': forms.Textarea(attrs={'rows': 1, 'cols': 10, 'class': 'form-control enlarge-on-focus'}),
    'product': forms.Textarea(attrs={'rows': 1, 'cols': 10, 'class': 'form-control enlarge-on-focus'}),
    'payment_date': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade', 'class': 'form-control'}),
    'purpose': forms.Textarea(attrs={'rows': 1, 'cols': 20, 'class': 'form-control enlarge-on-focus'}),
    'net_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'VAT_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'gross_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'claimed_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'rejected': forms.CheckboxInput(attrs={'class': 'form-control'}),
}
ExpenseFormset = inlineformset_factory(MP, Expense, fields=EXPENSE_FORMSET_FIELDS, widgets=EXPENSE_FORMSET_WDIGETS)
