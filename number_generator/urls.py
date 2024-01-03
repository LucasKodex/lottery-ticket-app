from django.urls import path
from . import views

app_name = "number_generator"

urlpatterns = [
    path("", views.RedirectToHomeView.as_view(), name="root_page"),
    path("home/", views.homeView, name="home_page"),
    path("generation/<int:pk>", views.GenerationDetailView.as_view(), name="generation_detail_page"),
    path("generation/", views.GenerationListView.as_view(), name="generation_listing_page"),
    path("about/", views.AboutView.as_view(), name="about_page"),
]
