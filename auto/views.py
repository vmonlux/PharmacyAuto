from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponse, FileResponse

from auto.forms import *
from .models import *

def backup(request):
    return render(request, 'backup.html')


def home(request):
    return render(request, 'home.html')

class OmnicellList(ListView):
    model = Omnicell
    context_object_name = 'omnicell_list'
    template_name = 'omnicell_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(OmnicellList, self).get_queryset()
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
    

class OmnicellView(UpdateView):
    model = Omnicell
    template_name = 'omnicell_view.html'
    form_class = OmnicellForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Refrigerators"] = Refrigerator.objects.filter(Omnicell=self.kwargs['pk'])
        context["Auxs"] = Aux.objects.filter(Omnicell=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmnicellView, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omnicellView", kwargs={'pk': pk})

class OmnicellUpdate(UpdateView):
    model = Omnicell
    template_name = 'omnicell_update.html'
    form_class = OmnicellForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmnicellUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewOmnicell", kwargs={'pk': pk})

class AuxList(ListView):
    model = Aux
    context_object_name = 'aux_list'
    template_name = 'aux_list.html'
    
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
    

class AuxView(UpdateView):
    model = Aux
    template_name = 'aux_view.html'
    form_class = AuxForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Aux Updated")
        return super(AuxView, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewAux", kwargs={'pk': pk})

class AuxUpdate(UpdateView):
    model = Aux
    template_name = 'aux_update.html'
    form_class = AuxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Aux Updated")
        return super(AuxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewAux", kwargs={'pk': pk})

class LockboxList(ListView):
    model = Lockbox
    context_object_name = 'lockbox_list'
    template_name = 'lockbox_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(LockboxList, self).get_queryset()
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
    

class LockboxView(UpdateView):
    model = Lockbox
    template_name = 'lockbox_view.html'
    form_class = LockboxForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Lockbox Updated")
        return super(LockboxView, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewLockbox", kwargs={'pk': pk})

class LockboxUpdate(UpdateView):
    model = Lockbox
    template_name = 'lockbox_update.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Updated")
        return super(LockboxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewLockbox", kwargs={'pk': pk})


class RefrigeratorList(ListView):
    model = Refrigerator
    context_object_name = 'refrigerator_list'
    template_name = 'refrigerator_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(RefrigeratorList, self).get_queryset()
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
    
class RefrigeratorView(UpdateView):
    model = Refrigerator
    template_name = 'refrigerator_view.html'
    form_class = RefrigeratorForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Refrigerator Updated")
        return super(RefrigeratorView, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("refrigeratorView", kwargs={'pk': pk})

class RefrigeratorUpdate(UpdateView):
    model = Refrigerator
    template_name = 'refrigerator_update.html'
    form_class = RefrigeratorForm
    
    def form_valid(self, form):
        messages.success(self.request, "Refrigerator Updated")
        return super(RefrigeratorUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("viewRefrigerator", kwargs={'pk': pk})
    

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