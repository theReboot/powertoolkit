from django.urls import path

from stats import views


urlpatterns = [
    path('chart/<int:year>/', views.get_data),
    path('download/<int:year>/', views.download),
    path('performance/', views.get_performance),
    path('remittance/', views.get_remittance),
    path('generation/', views.get_generation),
]
