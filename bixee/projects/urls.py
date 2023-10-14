from django.urls import path
from . import views

urlpatterns = [
    # project
    path('', views.projects, name='project'),
    path('add_project/', views.add_project, name='add_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/complete/', views.complete_project, name='complete_project'),
    # task
    path('<int:project_id>/task/', views.tasks, name='task'),
    path('<int:project_id>/add_task/', views.add_task, name='add_task'),
    path('<int:project_id>/task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:project_id>/task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:project_id>/task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('<int:project_id>/task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('<int:project_id>/task/<int:task_id>/toggle_important/', views.toggle_important, name='toggle_important'),

]
