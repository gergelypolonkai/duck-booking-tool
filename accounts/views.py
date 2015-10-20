# -*- coding: utf-8
"""
Views for the accounts module
"""

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm

class RegistrationFormView(generic.View):
    """
    Class to display the registration form
    """

    form_class = UserCreationForm
    template_name = 'accounts/registration.html'

    def get(self, request):
        """
        Implementation of the GET method
        """

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Implementation of the POST method
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('booking:list'))

        return render(request, self.template_name, {'form': form})
