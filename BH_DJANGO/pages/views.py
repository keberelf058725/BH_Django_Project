from django.http import HttpResponse
from django.shortcuts import render
from .Viv_Form import VivitrolForm

def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def viv_view(request, *args, **kwargs):
    return render(request, "viv.html", {})