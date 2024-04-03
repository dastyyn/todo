from django.urls import path
from todolist import views

urlpatterns = [
    path('api/v1/tasks', views.task_list_api_view),
    path('api/v1/tasks/<int:id>', views.task_detail_api_view),
]
