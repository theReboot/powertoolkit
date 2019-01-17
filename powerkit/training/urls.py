from django.urls import path

from training import views


urlpatterns = [
    path('start/', views.start_training, name='start_training'),
    path('continue/', views.continue_training, name='continue_training'),
    path('complete/<int:id>/', views.complete, name='complete_training'),
    path('select_answer/<int:id>/', views.select_answer, name='select_answer'),
]
