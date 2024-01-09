from django.urls import path, register_converter
from . import views, converters

register_converter(converters.SixDigitConverter, "dddddd")

app_name = "number_generator"

urlpatterns = [
    path("", views.RedirectToHomeView.as_view(), name="root_page"),
    path("home/", views.homeView, name="home_page"),
    path("generation/<dddddd:pk>/", views.GenerationDetailView.as_view(), name="generation_detail_page"),
    path("generation/", views.GenerationListView.as_view(), name="generation_listing_page"),
    path("about/", views.AboutView.as_view(), name="about_page"),
]
