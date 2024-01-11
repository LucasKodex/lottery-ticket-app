from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView, ListView, RedirectView, TemplateView
from django.db import IntegrityError, transaction
from django.http import HttpResponseNotFound

from .models import Generation

APP_NAME = "number_generator"

class RedirectToHomeView(RedirectView):
    pattern_name = f"{APP_NAME}:home_page"
    permanent = True

class HomeView(TemplateView):
    template_name = f"{APP_NAME}/home.html"

def homeViewPOST(request):
    TEMPLATE_NAME = f"{APP_NAME}/home.html"
    error_list = list()

    quantity = request.POST["quantity"]
    range_from = request.POST["range_from"]
    range_to = request.POST["range_to"]

    isQuantityInteger = quantity.isdecimal() or quantity[1:].isdecimal()
    isRangeFromInteger = range_from.isdecimal() or range_from[1:].isdecimal()
    isRangeToInteger = range_to.isdecimal() or range_to[1:].isdecimal()
    isInputInteger = isQuantityInteger and isRangeFromInteger and isRangeToInteger
    if not isInputInteger:
        error_list.append("Fields must be integer numbers.")
        return render(request, TEMPLATE_NAME, { "error_list": error_list })

    quantity = int(request.POST["quantity"])
    range_from = int(request.POST["range_from"])
    range_to = int(request.POST["range_to"])

    range_min = min(range_from, range_to)
    range_max = max(range_from, range_to)

    # checks for quantity erros
    isQuantityBelowOne = quantity < 1
    if isQuantityBelowOne:
        error_list.append("Quantity must be a positive integer above zero.")

    isQuantityGreaterThanOneHundred = quantity > 100
    if isQuantityGreaterThanOneHundred:
        error_list.append("Quantity must be equal or below 100.")

    # checks for ranges errors
    isStartingRangeBelowZero = range_min < 0
    if isStartingRangeBelowZero:
        error_list.append("The starting range must be a positive integer.")
    
    isEndingRangeAboveNinetyNine = range_max > 99
    if isEndingRangeAboveNinetyNine:
        error_list.append("The ending range must be equal or lower than 99.")

    range_size = range_max - range_min + 1
    isQuantityGreaterThanRangeSize = quantity > range_size
    if isQuantityGreaterThanRangeSize:
        error_list.append("Can not generate more numbers than exists within the specified range.")
    
    # return the feedback to user if there is any error
    hasErrorMessages = len(error_list) > 0
    if hasErrorMessages:
        return render(request, TEMPLATE_NAME, { "error_list": error_list })

    try:
        with transaction.atomic():
            generation = Generation()
            generation.range_from = range_min
            generation.range_to = range_max
            generation.save()

            randomNumbers = generation.generateRandomNumbers(quantity)
            for number in randomNumbers:
                number.save()
    except IntegrityError:
        error_list.append("Something went wrong :(. Contact an administrator and trying again later.")
        return render(request, TEMPLATE_NAME, { "error_list": error_list }, status=500)
    return redirect(
        "number_generator:generation_detail_page",
        pk=(generation.public_unique_identifier),
    )

def homeViewALL(request):
    TEMPLATE_NAME = f"{APP_NAME}/home.html"
    return render(request, TEMPLATE_NAME)

def homeView(request):
    if request.method == "POST":
        return homeViewPOST(request)
    return homeViewALL(request)

class GenerationDetailView(DetailView):
    template_name = f"{APP_NAME}/generation_detail.html"
    model = Generation

class GenerationListView(ListView):
    model = Generation
    template_name = f"{APP_NAME}/generation_list.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")

class AboutView(TemplateView):
    template_name = f"{APP_NAME}/about.html"
