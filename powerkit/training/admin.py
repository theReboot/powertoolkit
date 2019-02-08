from django.contrib import admin

from training.models import Training, TrainingSchedule, UserAnswer,\
    AssignmentAnswer


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['user', 'started', 'completed', 'percent_completion']


@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ['user_training', 'learning_page', 'current', 'completed']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'when']


@admin.register(AssignmentAnswer)
class AssignmentAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignment', 'completed', 'assessed']
