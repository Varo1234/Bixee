from django.db import models
from django.contrib.auth.models import User


# heredar modelo de usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', blank=True)
    position = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Projects(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(blank=True, null=True)
    fecha_entrega = models.DateField()
    completado = models.BooleanField(default=False)
    asignado_a = models.ForeignKey(User, on_delete=models.CASCADE)
    horas_trabajo = models.PositiveIntegerField(default=0)
    precio_proyecto = models.PositiveIntegerField(default=0)
    sobre_proyecto = models.TextField()
    tasks = models.ManyToManyField('Tasks', blank=True)

    def __str__(self):
        return self.nombre

    def get_tasks(self):
        return self.tasks.filter(deleted=False)

    def tasks_completed(self):
        return self.tasks.filter(completed=True, deleted=False).count()

    def tasks_total(self):
        return self.tasks.filter(deleted=False).count()

    def get_estado(self):
        task_completed = self.tasks_completed()
        task_total = self.tasks_total()
        if task_total - task_completed <= 0:
            return 'late'
        elif task_completed / task_total >= 0.5:
            return 'middle'
        else:
            return 'early'

    def progress(self):
        if self.tasks_total() == 0:
            return 0
        else:
            return int(self.tasks_completed() / self.tasks_total() * 100)


# Model for tasks in a project
class Tasks(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User)
    created_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    important = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

