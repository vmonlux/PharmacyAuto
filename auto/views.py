from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

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