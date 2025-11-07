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
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import PasswordResetConfirmView

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

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.user
        login(self.request, user)
        return response

class UserList(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'db/account/account_list.html'
    context_object_name = "object"
    
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
    template_name = 'db/account/account_create.html'
    form_class = UserCreateForm
    context_object_name = "object"
    
    def get_initial(self):
        initial = super().get_initial()
        random_password = User.objects.make_random_password()
        initial['password1'] = random_password
        initial['password2'] = random_password
        return initial
    
    def form_valid(self, form):
        form.instance.email = form.cleaned_data['username']
        random_password = User.objects.make_random_password()
        form.instance.password1 = random_password
        form.instance.password2 = random_password
        user = form.save(commit=False)

        user.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('account-view', kwargs={'pk': self.object.pk})
    
class UserView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'db/account/account_view.html'
    context_object_name = "object"

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'db/account/account_update.html'
    context_object_name = "object"
    
    def get_success_url(self):
        url = reverse('account-view', kwargs={'pk':self.object.pk})
        return url

class OmniList(LoginRequiredMixin, ListView):
    model = Omnicell
    template_name = 'db/omni/omni_list.html'
    
    def get_queryset(self):
        org = self.request.user.Org
        query = self.request.GET.get("q")
        queryset = super(OmniList, self).get_queryset()
        if query == None:
            return queryset.filter(Org=org)
        elif query == "emergency":
            filter = queryset.filter(Emergency=True)
            return filter.filter(Org=org)
        else:
            filter = queryset.filter(
                Q(Omni_Id__icontains=query) |
                Q(Omni_Description__icontains=query) |
                Q(Building__Name__icontains=query) |
                Q(Area__icontains=query) |
                Q(Serial_Number__icontains=query) |
                Q(Model__Model__icontains=query)
            )
            return filter.filter(Org=org)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class OmniView(LoginRequiredMixin, DetailView):
    model = Omnicell
    template_name = 'db/omni/omni_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Refrigerators"] = Refrigerator.objects.filter(Omnicell=self.kwargs['pk'])
        context["Auxs"] = Aux.objects.filter(Omnicell=self.kwargs['pk'])
        context["Requests"] = ServiceItem.objects.exclude(Solved=True).filter(Omnicell=self.kwargs['pk'])
        context["Logs"] = ServiceItem.objects.exclude(Solved=False).filter(Omnicell=self.kwargs['pk']).order_by('-Closed')
        return context

class OmniCreate(LoginRequiredMixin, CreateView):
    model = Omnicell
    template_name = 'db/omni/omni_create.html'
    form_class = OmnicellCreateForm
    
    def get_initial(self):
        org = self.request.user.Org
        initial = super().get_initial()
        initial["Org"] = org
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(OmniCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})

class OmniUpdate(LoginRequiredMixin, UpdateView):
    model = Omnicell
    template_name = 'db/omni/omni_update.html'
    form_class = OmnicellForm
    
    def get_initial(self):
        org = self.request.user.Org
        initial = super().get_initial()
        if self.object.Org is None:
            initial["Org"] = org
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmniUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omni-view", kwargs={'pk': self.object.pk})

class AuxList(LoginRequiredMixin, ListView):
    model = Aux
    template_name = 'db/auxx/aux_list.html'
    
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
    template_name = 'db/auxx/aux_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AuxUpdate(LoginRequiredMixin, UpdateView):
    model = Aux
    template_name = 'db/auxx/aux_update.html'
    form_class = AuxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Aux Updated")
        return super(AuxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("aux-view", kwargs={'pk': pk})

class BoxList(LoginRequiredMixin, ListView):
    model = Lockbox
    template_name = 'db/box/box_list.html'
    
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
    template_name = 'db/box/box_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class BoxCreate(LoginRequiredMixin, CreateView):
    model = Lockbox
    template_name = 'db/box/box_create.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Created")
        return super(BoxCreate, self).form_valid(form)
    
    def get_success_url(self):

        return reverse_lazy("box-view", kwargs={'pk': self.object.pk})
    
class BoxUpdate(LoginRequiredMixin, UpdateView):
    model = Lockbox
    template_name = 'db/box/box_update.html'
    form_class = LockboxForm
    
    def form_valid(self, form):
        messages.success(self.request, "Lockbox Updated")
        return super(BoxUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("box-view", kwargs={'pk': pk})

class RefList(LoginRequiredMixin, ListView):
    model = Refrigerator
    template_name = 'db/ref/ref_list.html'
    
    def get_queryset(self):
        org = self.request.user.Org
        query = self.request.GET.get("q")
        queryset = super(RefList, self).get_queryset()
        if query == None:
            return queryset.filter(Org=org)
        elif query =="none":
            filter = queryset.filter(Model=None)
            return filter.filter(Org=org)
        else:
            filter = queryset.filter(
                Q(Facilities_Id__icontains=query) |
                Q(Omnicell__Omni_Id__icontains=query) |
                Q(Omnicell__Omni_Description__icontains=query) |
                Q(Type__icontains=query) |
                Q(Model__ModelName__icontains=query) |
                Q(Model__Category__icontains=query)
            )
            return filter.filter(Org=org)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class RefView(LoginRequiredMixin, DetailView):
    model = Refrigerator
    template_name = 'db/ref/ref_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RefCreate(LoginRequiredMixin, CreateView):
    model = Refrigerator
    template_name = 'db/ref/ref_create.html'
    form_class = RefrigeratorCreateForm
    
    def get_initial(self):
        org = self.request.user.Org
        initial = super().get_initial()
        initial["Org"] = org
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Created")
        return super(RefCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("ref-view", kwargs={'pk': self.object.pk})
    
class RefUpdate(LoginRequiredMixin, UpdateView):
    model = Refrigerator
    template_name = 'db/ref/ref_update.html'
    form_class = RefrigeratorForm
    
    def get_initial(self):
        org = self.request.user.Org
        initial = super().get_initial()
        if self.object.Org is None:
            initial["Org"] = org
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, "Refrigerator Updated")
        return super(RefUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("ref-view", kwargs={'pk': self.object.pk})

class SrList(LoginRequiredMixin, ListView):
    model = ServiceItem
    template_name = 'db/sr/sr_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super(SrList, self).get_queryset()
        if query == None:
            return queryset
        else:
            
            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class SrView(LoginRequiredMixin, DetailView):
    model = ServiceItem
    template_name = 'db/sr/sr_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SrCreate(LoginRequiredMixin, CreateView):
    model = ServiceItem
    template_name = 'db/sr/sr_create.html'
    form_class = ServiceItemForm
    
    def get_initial(self):
        initial = super().get_initial()
        o = self.request.GET['o']
        if o:
            initial['Omnicell'] = o
        initial["Opened_By"] = self.request.user
        now = datetime.now()
        initial["Opened"] = now.strftime("%Y-%m-%d %H:%M:%S")
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, "Service Request Created")
        return super(SrCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("omni-view", kwargs={'pk': self.object.Omnicell.pk})
    
class SrUpdate(LoginRequiredMixin, UpdateView):
    model = ServiceItem
    template_name = 'db/sr/sr_update.html'
    form_class = ServiceItemForm
    
    def form_valid(self, form):
        messages.success(self.request, "Service Request Updated")
        return super(SrUpdate, self).form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("omni-view", kwargs={'pk': self.object.Omnicell.pk})


# Master table views

class OmniMaster(LoginRequiredMixin, ListView):
    model = Omnicell
    template_name='db/omni/omni_table.html'

class FlexMaster(LoginRequiredMixin, ListView):
    model = Refrigerator
    template_name='flex_table.html'

class LockMaster(LoginRequiredMixin, ListView):
    model = Lockbox
    template_name='db/box/lockbox_table.html'

class AuxMaster(LoginRequiredMixin, ListView):
    model = Aux
    template_name='db/auxx/aux_table.html'

# Dashboard Views

class DashView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = self.request.user.Org
        omnis = Omnicell.objects.all()
        
        # CT Upgrade Hooks
        upgrades = omnis.exclude(CT_Version='28.5.13.21')
        nt = upgrades.filter(Building__Name="NT").count()
        nt_tot = omnis.filter(Building__Name="NT").count()
        st = upgrades.filter(Building__Name="ST").count()
        st_tot = omnis.filter(Building__Name="ST").count()
        ub = upgrades.filter(Building__Name="HVN").count()
        ub_tot = omnis.filter(Building__Name="HVN").count()
        omni_tot = omnis.count()
        total = upgrades.count()
        offsite = total - nt - st - ub
        offsite_tot = omni_tot - nt_tot - st_tot - ub_tot
        context["Upgrades"] = upgrades
        context["Total"] = total
        context["Omni_Tot"] = omni_tot
        context["Omni_Rem"] = omni_tot - total
        context["NT"] = nt
        context["NT_Tot"] = nt_tot
        context["NT_Rem"] = nt_tot - nt
        context["ST"] = st
        context["ST_Tot"] = st_tot
        context["ST_Rem"] = st_tot - st
        context["UB"] = ub
        context["UB_Tot"] = ub_tot
        context["UB_Rem"] = ub_tot - ub
        context["OFF"] = offsite
        context["OFF_Tot"] = offsite_tot
        context["OFF_Rem"] = offsite_tot - offsite
        
        # SR Hooks
        requests = ServiceItem.objects.exclude(Solved=True).order_by('Omnicell')
        context["Requests"] = requests
    
        # Spare/Repair/Dead Fridge Hooks
        spare = Refrigerator.objects.filter(Org=org, Omnicell=None, Broken=False)
        context["Spare"] = spare
        broken = Refrigerator.objects.filter(Org=org, Broken=True)
        context["Repair"] = broken
        

        return context

class OmniDashUpdate(LoginRequiredMixin, UpdateView):
    model = Omnicell
    template_name = 'db/omni/omni_update.html'
    form_class = OmnicellForm
    
    def form_valid(self, form):
        messages.success(self.request, "Omnicell Updated")
        return super(OmniDashUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("dash")

class OmniInspect(TemplateView):
    template_name = 'dash/form/inspection.html'