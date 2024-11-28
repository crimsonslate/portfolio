from django.urls import path

from . import views

urlpatterns = [
    path("gallery/", views.PortfolioGalleryView.as_view(), name="portfolio gallery"),
    path("contact/", views.PortfolioContactView.as_view(), name="portfolio contact"),
    path("upload/", views.PortfolioUploadView.as_view(), name="portfolio upload"),
    path("search/", views.PortfolioSearchView.as_view(), name="portfolio search"),
    path("login/", views.PortfolioLoginView.as_view(), name="portfolio login"),
    path("logout/", views.PortfolioLogoutView.as_view(), name="portfolio logout"),
    path("<str:slug>/", views.MediaDetailView.as_view(), name="media detail"),
    path("<str:slug>/edit/", views.MediaUpdateView.as_view(), name="media edit"),
    path("<str:slug>/delete/", views.MediaDeleteView.as_view(), name="media delete"),
]
