from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from auto.forms import *
from .models import *


def home(request):
    return render(request, 'home.html')

class OmnicellList(ListView):
    model = Omnicell
    context_object_name = 'omnicell_list'
    template_name = 'omnicell_list.html'
    
    def get_queryset(self):
        queryset = super(OmnicellList, self).get_queryset()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class OmnicellUpdate(UpdateView):
    model = Omnicell
    template_name = 'omnicell_update.html'
    form_class = OmnicellForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmnicellUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omnicell", kwargs={'pk': pk})