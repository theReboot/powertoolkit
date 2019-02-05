from django.urls import path

from training import views


urlpatterns = [
    path('start/', views.start_training, name='start_training'),
    path('continue/', views.continue_training, name='continue_training'),
    path('complete/<int:id>/', views.complete, name='complete_training'),
    path('select_answer/<int:id>/', views.select_answer, name='select_answer'),
    path('intro/<int:id>/', views.get_intro, name='get_intro'),
    path('question/<int:id>/', views.get_question, name='get_question'),
    path('sessions/<int:id>/', views.get_sessions),
    path('assignment/<int:id>/', views.assignment, name='assignment'),
    #path('assignment/<int:id>/', views.get_assignment),
]
