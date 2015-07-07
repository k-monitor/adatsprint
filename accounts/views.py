from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from braces.views import MessageMixin


def logout(request):
    messages.success(request, _("Logged out successfully. Thanks for helping out!"))
    return auth_views.logout(request, next_page=reverse('campaigns:landing'))


class RegisterView(MessageMixin, generic.CreateView):
    template_name = 'accounts/register.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        self.messages.success(_("User account created. You can now log in."))
        return response
