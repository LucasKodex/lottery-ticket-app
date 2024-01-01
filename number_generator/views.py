from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, RedirectView, TemplateView

APP_NAME = "number_generator"

class RedirectToHomeView(RedirectView):
    pattern_name = f"{APP_NAME}:home_page"
    permanent = True

# class HomeView(FormView):
class HomeView(TemplateView):
    template_name = f"{APP_NAME}/home.html"

# class GenerationDetailView(DetailView):
class GenerationDetailView(TemplateView):
    template_name = f"{APP_NAME}/generation_detail.html"

# class GenerationListView(ListView):
class GenerationListView(TemplateView):
    template_name = f"{APP_NAME}/generation_list.html"

class AboutView(TemplateView):
    template_name = f"{APP_NAME}/about.html"
