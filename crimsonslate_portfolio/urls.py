from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("gallery/", views.MediaGalleryView.as_view(), name="gallery"),
    path("search/", views.MediaSearchView.as_view(), name="search"),
    path("results/", views.MediaSearchResultsView.as_view(), name="search results"),
    path("files/", views.SourceFileListView.as_view(), name="list files"),
    path("files/new/", views.SourceFileCreateView.as_view(), name="create file"),
    path("files/<int:pk>/", views.SourceFileDetailView.as_view(), name="detail file"),
    path(
        "files/<int:pk>/update/",
        views.SourceFileUpdateView.as_view(),
        name="update file",
    ),
    path(
        "files/<int:pk>/delete/",
        views.SourceFileDeleteView.as_view(),
        name="delete file",
    ),
    path("<int:pk>/create/", views.MediaCreateView.as_view(), name="create media"),
    path("<str:slug>/", views.MediaDetailView.as_view(), name="detail media"),
    path("<str:slug>/delete/", views.MediaDeleteView.as_view(), name="delete media"),
    path("<str:slug>/update/", views.MediaUpdateView.as_view(), name="update media"),
]
