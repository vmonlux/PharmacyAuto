from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from auto.forms import *
from .models import *


def home(request):
    return render(request, 'home.html')

# class OmnicellList(ListView):
    