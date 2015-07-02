from django import forms

from .models import MP


class BaseMPForm(forms.ModelForm):
    class Meta:
        model = MP
        fields = [
            'agreement_number',
            'campaign_start',
            'campaign_end',
            'total',
            'signed_on',
            'comment',
        ]


class MPProcessForm(BaseMPForm):
    def save(self, commit=True):
        instance = super(MPProcessForm, self).save(commit=False)
        instance.status = MP.STATUS.PROCESSED
        if commit:
            instance.save()

        return instance


class MPVerifyForm(BaseMPForm):
    def save(self, commit=True):
        instance = super(MPVerifyForm, self).save(commit=False)
        instance.status = MP.STATUS.VERIFIED
        if commit:
            instance.save()

        return instance
