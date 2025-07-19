from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, default = 1)
    assigned_to = models.ManyToManyField(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #taskdetils_set = models.OneToOneField('TaskDetails', on_delete=models.CASCADE, null=True, blank=True)

class TaskDetails(models.Model):
        HIGH = 'H'
        MEDIUM = 'M'
        LOW = 'L'
        PRIORITY_OPTIONS = (
            (LOW, 'Low'),
            (MEDIUM, 'Medium'),
            (HIGH, 'High'),
        )
        task = models.OneToOneField(
             Task, 
             on_delete=models.CASCADE,
             related_name='details',
        )
        assigned_to = models.CharField(max_length=100)
        priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)

class Project(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateField()
