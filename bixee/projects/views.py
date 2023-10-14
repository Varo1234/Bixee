from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datetime_safe import datetime

from .models import Projects, UserProfile, Tasks
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect


# list of projects
@login_required
def projects(request):
    # pasarle a la plantilla los proyectos
    proyectos = Projects.objects.all()
    users = User.objects.all()
    proyectos_data = [{'proyecto': proyecto, 'estado': proyecto.get_estado()} for proyecto in proyectos]
    print(proyectos_data)
    return render(request, 'pages/application/project/list.html', {'proyectos': proyectos_data, 'users': users})


# project details page
@login_required
def project_detail(request, project_id):
    proyecto = Projects.objects.get(id=project_id)
    asignado_a = User.objects.get(id=proyecto.asignado_a.id)
    tasks = proyecto.get_tasks()
    tareas_completadas = proyecto.tasks_completed()
    tareas_totales = proyecto.tasks_total()
    progress = proyecto.progress()
    return render(request, 'pages/application/project/details.html', {'proyecto': proyecto, 'asignado_a': asignado_a,
                                                                      'tasks': tasks,
                                                                      'tareas_completadas': tareas_completadas,
                                                                      'tareas_totales': tareas_totales,
                                                                      'progress': progress})


@login_required
def add_project(request):
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_entrega = request.POST.get('fecha_entrega')
    asignado_a = request.POST.get('asignado_a')
    precio_proyecto = request.POST.get('precio_proyecto')
    sobre_proyecto = request.POST.get('sobre_proyecto')

    asignado_a = User.objects.get(username=asignado_a)
    # fecha de inicio 19 October 2023 cambiar a 2023-10-19
    fecha_inicio = datetime.strptime(fecha_inicio, '%d %B %Y').strftime('%Y-%m-%d')
    # fecha de entrega 19 October 2023 cambiar a 2023-10-19
    fecha_entrega = datetime.strptime(fecha_entrega, '%d %B %Y').strftime('%Y-%m-%d')

    proyecto = Projects.objects.create(nombre=nombre,
                                       descripcion=descripcion,
                                       fecha_inicio=fecha_inicio if fecha_inicio else None,
                                       fecha_entrega=fecha_entrega if fecha_entrega else None,
                                       precio_proyecto=precio_proyecto if precio_proyecto else None,
                                       sobre_proyecto=sobre_proyecto if sobre_proyecto else "",
                                       asignado_a=asignado_a)
    proyecto.save()
    return redirect(request.META.get('HTTP_REFERER', '/fallback/url/'))


@login_required
def complete_project(request, project_id):
    proyecto = Projects.objects.get(id=project_id)
    proyecto.completado = not proyecto.completado
    proyecto.save()
    print(proyecto.completado)
    return redirect(request.META.get('HTTP_REFERER', '/fallback/url/'))


@login_required
def task_detail(request, project_id, task_id):
    proyecto = Projects.objects.get(id=project_id)
    task = proyecto.tasks.get(id=task_id)
    asignado_a = User.objects.get(id=task.assigned_to.id)
    return render(request, 'pages/application/task/task.html', {'proyecto': proyecto, 'asignado_a': asignado_a,
                                                                'task': task})


@login_required
def tasks(request, project_id):
    proyecto = Projects.objects.get(id=project_id)
    all_tasks = proyecto.tasks.filter(deleted=False)
    important_tasks = proyecto.tasks.filter(important=True, deleted=False)
    completed_tasks = proyecto.tasks.filter(completed=True, deleted=False)
    deleted_tasks = proyecto.tasks.filter(deleted=True)
    return render(request, 'pages/application/task/task.html', {'proyecto': proyecto,
                                                                'tasks': all_tasks,
                                                                'important_tasks': important_tasks,
                                                                'completed_tasks': completed_tasks,
                                                                'deleted_tasks': deleted_tasks
                                                                })


@login_required
def edit_task(request, project_id, task_id):
    if request.method == "POST":
        task = get_object_or_404(Tasks, id=task_id)
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.save()

        return redirect(request.META.get('HTTP_REFERER', '/fallback/url/'))


@login_required
def delete_task(request, project_id, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.deleted = True
    task.save()

    return redirect(request.META.get('HTTP_REFERER', '/fallback/url/'))


@login_required
def add_task(request, project_id):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        proyecto = Projects.objects.get(id=project_id)
        task = Tasks.objects.create(name=name, description=description)
        task.assigned_to = proyecto.asignado_a.id
        proyecto.tasks.add(task)
        proyecto.save()
        task.save()

        return redirect(request.META.get('HTTP_REFERER', '/fallback/url/'))


@login_required
def toggle_task(request, project_id, task_id):
    if request.method == "POST":
        proyecto = Projects.objects.get(id=project_id)
        task = get_object_or_404(proyecto.tasks, id=task_id)
        completed = request.POST.get('completed') == 'true'
        task.completed = completed
        task.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Task updated successfully.'
        })


@login_required
def toggle_important(request, project_id, task_id):
    if request.method == "POST":
        proyecto = Projects.objects.get(id=project_id)
        task = get_object_or_404(proyecto.tasks, id=task_id)
        task.important = not task.important  # Cambia el estado de important
        task.save()

        return JsonResponse({
            'status': 'success',
            'important': task.important
        })
