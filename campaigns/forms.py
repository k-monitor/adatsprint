from django import forms
from django.forms.models import inlineformset_factory

from .models import MP, Expense


class BaseMPForm(forms.ModelForm):
    NEXT_STATUS = None

    def __init__(self, *args, **kwargs):
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
        instance.status = MP.STATUS.PROCESSED
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

    def get_formset_kwargs(self):
        assert self.instance is not None
        kwargs = super(MPProcessForm, self).get_formset_kwargs()
        kwargs['extra'] = (self.instance.pdf_page_count or 1) * 8
        return kwargs


class MPVerifyForm(BaseMPForm):
    NEXT_STATUS = MP.STATUS.VERIFIED

    def get_formset_kwargs(self):
        assert self.instance is not None
        kwargs = super(MPVerifyForm, self).get_formset_kwargs()
        kwargs['extra'] = 0
        return kwargs


EXPENSE_FORMSET_FIELDS = [
    'row_number',
    'invoice_reference',
    'delivery_date',
    'provider',
    'product',
    'purchase_date',
    'purpose',
    'net_amount',
    'VAT_amount',
    'gross_amount',
    'claimed_amount',
]
EXPENSE_FORMSET_WDIGETS = {
    'row_number': forms.TextInput(attrs={'size': 2, 'class': 'form-control'}),
    'invoice_reference': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'delivery_date': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade', 'class': 'form-control'}),
    'provider': forms.TextInput(attrs={'size': 10, 'class': 'form-control'}),
    'product': forms.TextInput(attrs={'size': 10, 'class': 'form-control'}),
    'purchase_date': forms.DateInput(attrs={'data-provide': 'datepicker', 'data-date-format': 'yyyy-mm-dd', 'data-date-autoclose': 'true', 'data-date-start-view': 'decade', 'class': 'form-control'}),
    'purpose': forms.TextInput(attrs={'size': 20, 'class': 'form-control'}),
    'net_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'VAT_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'gross_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
    'claimed_amount': forms.TextInput(attrs={'size': 8, 'class': 'form-control'}),
}
ExpenseFormset = inlineformset_factory(MP, Expense, fields=EXPENSE_FORMSET_FIELDS, widgets=EXPENSE_FORMSET_WDIGETS)
