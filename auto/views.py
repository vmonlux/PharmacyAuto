from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.db.models import Q
from django.http import HttpResponse, FileResponse

from auto.forms import *
from .models import *

def backup(request):
    return render(request, 'backup.html')

class TestView(ListView):
    model = Omnicell
    template_name="test.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(TestView, self).get_queryset()
        if query == None:
            return queryset
        elif query == "emergency":
            filter = queryset.filter(Emergency=True)
            return filter
        else:
            filter = queryset.filter(
                Q(Omni_Id__icontains=query) |
                Q(Omni_Description__icontains=query) |
                Q(Building__Name__icontains=query) |
                Q(Area__icontains=query) |
                Q(Serial_Number__icontains=query) |
                Q(Model__Model__icontains=query)
            )
            return filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def home(request):
    return render(request, 'home.html')

class OmniList(ListView):
    model = Omnicell
    template_name = 'omni/omni_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(OmniList, self).get_queryset()
        if query == None:
            return queryset
        elif query == "emergency":
            filter = queryset.filter(Emergency=True)
            return filter
        else:
            filter = queryset.filter(
                Q(Omni_Id__icontains=query) |
                Q(Omni_Description__icontains=query) |
                Q(Building__Name__icontains=query) |
                Q(Area__icontains=query) |
                Q(Serial_Number__icontains=query) |
                Q(Model__Model__icontains=query)
            )
            return filter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class OmniView(DetailView):
    model = Omnicell
    template_name = 'omni/omni_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Refrigerators"] = Refrigerator.objects.filter(Omnicell=self.kwargs['pk'])
        context["Auxs"] = Aux.objects.filter(Omnicell=self.kwargs['pk'])
        return context

class OmniCreate(CreateView):
    model = Omnicell
    template_name = 'omni/omni_create.html'
    form_class = OmnicellCreateForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(OmniCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})

class OmniUpdate(UpdateView):
    model = Omnicell
    template_name = 'omni/omni_update.html'
    form_class = OmnicellForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmniUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omni-view", kwargs={'pk': pk})

class AuxList(ListView):
    model = Aux
    template_name = 'auxx/aux_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(AuxList, self).get_queryset()
        if query == None:
            return queryset
        else:
            filter = queryset.filter(
                Q(Omnicell__Omni_Id__icontains=query) |
                Q(Omnicell__Omni_Description__icontains=query) |
                Q(Omnicell__Building__Name__icontains=query) |
                Q(Omnicell__Area__icontains=query) |
                Q(Serial_Number__icontains=query) |
                Q(Model__Model__icontains=query)
            )
            return filter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class AuxView(DetailView):
    model = Aux
    template_name = 'aux/aux_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AuxUpdate(UpdateView):
    model = Aux
    template_name = 'aux_update.html'
    form_class = AuxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Aux Updated")
        return super(AuxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("aux-view", kwargs={'pk': pk})

class BoxList(ListView):
    model = Lockbox
    template_name = 'box/box_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(BoxList, self).get_queryset()
        if query == None:
            return queryset
        else:
            filter = queryset.filter(
                Q(Refrigerator__Omnicell__Omni_Id__icontains=query) |
                Q(Refrigerator__Omnicell__Omni_Description__icontains=query) |
                Q(Refrigerator__Omnicell__Building__Name__icontains=query) |
                Q(Refrigerator__Omnicell__Area__icontains=query) |
                Q(Medication__icontains=query)
            )
            return filter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class BoxView(DetailView):
    model = Lockbox
    template_name = 'box_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class BoxUpdate(UpdateView):
    model = Lockbox
    template_name = 'box/box_update.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Updated")
        return super(BoxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("box-view", kwargs={'pk': pk})

class RefList(ListView):
    model = Refrigerator
    template_name = 'ref/ref_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(RefList, self).get_queryset()
        if query == None:
            return queryset
        elif query =="none":
            filter = queryset.filter(Model=None)
            return filter
        else:
            filter = queryset.filter(
                Q(Facilities_Id__icontains=query) |
                Q(Omnicell__Omni_Id__icontains=query) |
                Q(Omnicell__Omni_Description__icontains=query) |
                Q(Type__icontains=query) |
                Q(Model__ModelName__icontains=query) |
                Q(Model__Category__icontains=query)
            )
            return filter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class RefView(DetailView):
    model = Refrigerator
    template_name = 'ref/ref_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RefCreate(CreateView):
    model = Refrigerator
    template_name = 'ref/ref_create.html'
    form_class = RefrigeratorCreateForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(OmniCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})
    
class RefUpdate(UpdateView):
    model = Refrigerator
    template_name = 'ref/ref_update.html'
    form_class = RefrigeratorForm
    
    def form_valid(self, form):
        messages.success(self.request, "Refrigerator Updated")
        return super(RefUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("ref-view", kwargs={'pk': pk})
    

# Master table views

class OmniMaster(ListView):
    model = Omnicell
    template_name='omni_table.html'

class FlexMaster(ListView):
    model = Refrigerator
    template_name='flex_table.html'

class LockMaster(ListView):
    model = Lockbox
    template_name='lockbox_table.html'

class AuxMaster(ListView):
    model = Aux
    template_name='aux_table.html'