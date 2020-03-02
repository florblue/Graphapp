# Create your views here.
from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Person
from graphapp import db

class PersonDetailView(DetailView):

    model = Person


class PersonListView(ListView):

    model = Person


def index(request):
    return render(request, 'index.html')
