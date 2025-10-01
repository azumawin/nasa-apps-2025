from django.contrib import admin
from django.urls import path

from asteroid import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/asteroid/",
        views.AsteroidListView.as_view(),
        name="asteroid_list_view",
    ),
]
