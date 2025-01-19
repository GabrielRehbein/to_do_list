from django.urls import path
from .views import TaskListCreateAPIView,  TaskRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task_list_create'),
    path('tasks/<int:id>',
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name='task_retrieve_update_destroy'
    ),
]
