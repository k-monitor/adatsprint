from django.contrib import admin

from .models import Campaign, MP, Expense


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'completion_rate_pcent', 'verification_rate_pcent')

    def completion_rate_pcent(self, obj):
        return '{:.2f}%'.format(100 * obj.completion_rate)
    completion_rate_pcent.short_description = "Completion"

    def verification_rate_pcent(self, obj):
        return '{:.2f}%'.format(100 * obj.verification_rate)
    verification_rate_pcent.short_description = "Verification"


class ExpenseInline(admin.TabularInline):
    model = Expense


@admin.register(MP)
class MPAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'name', 'agreement_number', 'total')
    search_fields = ['name']
    list_filter = ['status']
    inlines = [ExpenseInline]
