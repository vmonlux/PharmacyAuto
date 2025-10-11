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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

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

# Database User Object

class UserList(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'account/account_list.html'
    
    def get_queryset(self):
        set = super().get_queryset()
        query = self.request.GET.get('q')
        queryset = set.filter(is_active=True)
        if query:
            filter = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            return filter
        else:
            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['query'] = query
        return context
    
class UserCreate(LoginRequiredMixin, CreateView):
    model = get_user_model()
    template_name = 'account/account_create.html'
    form_class = UserCreateForm
    
    def get_success_url(self):
        return reverse_lazy('account-view', kwargs={'pk': self.object.pk})
    
class UserView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'account/account_view.html'

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'account/account_update.html'
    
    def get_success_url(self):
        url = reverse('account-view', kwargs={'pk':self.object.pk})
        return url

class OmniList(LoginRequiredMixin, ListView):
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
    
class OmniView(LoginRequiredMixin, DetailView):
    model = Omnicell
    template_name = 'omni/omni_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Refrigerators"] = Refrigerator.objects.filter(Omnicell=self.kwargs['pk'])
        context["Auxs"] = Aux.objects.filter(Omnicell=self.kwargs['pk'])
        return context

class OmniCreate(LoginRequiredMixin, CreateView):
    model = Omnicell
    template_name = 'omni/omni_create.html'
    form_class = OmnicellCreateForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(OmniCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})

class OmniUpdate(LoginRequiredMixin, UpdateView):
    model = Omnicell
    template_name = 'omni/omni_update.html'
    form_class = OmnicellForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmniUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omni-view", kwargs={'pk': pk})

class AuxList(LoginRequiredMixin, ListView):
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
    
class AuxView(LoginRequiredMixin, DetailView):
    model = Aux
    template_name = 'aux/aux_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AuxUpdate(LoginRequiredMixin, UpdateView):
    model = Aux
    template_name = 'aux_update.html'
    form_class = AuxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Aux Updated")
        return super(AuxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("aux-view", kwargs={'pk': pk})

class BoxList(LoginRequiredMixin, ListView):
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
    
class BoxView(LoginRequiredMixin, DetailView):
    model = Lockbox
    template_name = 'box/box_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class BoxCreate(LoginRequiredMixin, CreateView):
    model = Lockbox
    template_name = 'box/box_create.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Created")
        return super(BoxCreate, self).form_valid(form)
    
    def get_success_url(self):

        return reverse_lazy("box-view", kwargs={'pk': self.object.pk})
    
class BoxUpdate(LoginRequiredMixin, UpdateView):
    model = Lockbox
    template_name = 'box/box_update.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Updated")
        return super(BoxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("box-view", kwargs={'pk': pk})

class RefList(LoginRequiredMixin, ListView):
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
    
class RefView(LoginRequiredMixin, DetailView):
    model = Refrigerator
    template_name = 'ref/ref_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RefCreate(LoginRequiredMixin, CreateView):
    model = Refrigerator
    template_name = 'ref/ref_create.html'
    form_class = RefrigeratorCreateForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(RefCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})
    
class RefUpdate(LoginRequiredMixin, UpdateView):
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

class OmniMaster(LoginRequiredMixin, ListView):
    model = Omnicell
    template_name='omni_table.html'

class FlexMaster(LoginRequiredMixin, ListView):
    model = Refrigerator
    template_name='flex_table.html'

class LockMaster(LoginRequiredMixin, ListView):
    model = Lockbox
    template_name='lockbox_table.html'

class AuxMaster(LoginRequiredMixin, ListView):
    model = Aux
    template_name='aux_table.html'