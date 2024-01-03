from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView, ListView, RedirectView, TemplateView
from django.db import IntegrityError, transaction

from .models import Generation

APP_NAME = "number_generator"

class RedirectToHomeView(RedirectView):
    pattern_name = f"{APP_NAME}:home_page"
    permanent = True

class HomeView(TemplateView):
    template_name = f"{APP_NAME}/home.html"

def homeViewPOST(request):
    TEMPLATE_NAME = f"{APP_NAME}/home.html"

    quantity = request.POST["quantity"]
    range_from = request.POST["range_from"]
    range_to = request.POST["range_to"]

    isInputDecimal = quantity.isdecimal() and range_from.isdecimal() and range_to.isdecimal()
    if not isInputDecimal:
        return render(
            request,
            TEMPLATE_NAME,
            {
                "error_list": [ "Fields must be integer numbers." ],
            },
        )

    quantity = int(request.POST["quantity"])
    range_from = int(request.POST["range_from"])
    range_to = int(request.POST["range_to"])

    try:
        with transaction.atomic():
            generation = Generation()
            generation.range_from = range_from
            generation.range_to = range_to
            generation.save()

            randomNumbers = generation.generateRandomNumbers(quantity)
            for number in randomNumbers:
                number.save()
    except IntegrityError:
        return render(
            request,
            TEMPLATE_NAME,
            context={
                "error_list": [
                    "Something went wrong :(. Contact an \
                    administrator and trying again later."
                ],
            },
            status=500,
        )
    return redirect(
        "number_generator:generation_detail_page",
        args=(generation.public_unique_identifier),
    )

def homeViewALL(request):
    TEMPLATE_NAME = f"{APP_NAME}/home.html"
    return render(request, TEMPLATE_NAME)

def homeView(request):
    if request.method == "POST":
        return homeViewPOST(request)
    return homeViewALL(request)

# class GenerationDetailView(DetailView):
class GenerationDetailView(TemplateView):
    template_name = f"{APP_NAME}/generation_detail.html"

# class GenerationListView(ListView):
class GenerationListView(TemplateView):
    template_name = f"{APP_NAME}/generation_list.html"

class AboutView(TemplateView):
    template_name = f"{APP_NAME}/about.html"
