from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, RedirectView, TemplateView
from .models import Generation, Number

APP_NAME = "number_generator"

class RedirectToHomeView(RedirectView):
    pattern_name = f"{APP_NAME}:home_page"
    permanent = True

# class HomeView(FormView):
class HomeView(TemplateView):
    template_name = f"{APP_NAME}/home.html"

class GenerationDetailView(DetailView):
    template_name = f"{APP_NAME}/generation_detail.html"
    model = Generation

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(public_unique_identifier=pk)

# class GenerationListView(ListView):
class GenerationListView(TemplateView):
    template_name = f"{APP_NAME}/generation_list.html"

class AboutView(TemplateView):
    template_name = f"{APP_NAME}/about.html"
