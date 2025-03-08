from django.urls import path
from . import views

urlpatterns = [
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/categories/<int:category_id>/subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/upload-csv/', views.upload_csv, name='upload_csv'),
]