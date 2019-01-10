from django.urls import path

from training import views


urlpatterns = [
    path('start/', views.start_training, name='start_training'),
    path('continue/', views.continue_training, name='continue_training'),
    path('complete/', views.complete, name='complete_training'),
]
