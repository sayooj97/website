# urls.py
from django.urls import path
from .views import get_filtered_pc_builds

urlpatterns = [
    path('api/filtered-pc-builds/', get_filtered_pc_builds),  # API to fetch a random filtered build
]