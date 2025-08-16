from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
         ('PENDING', 'Pending'),
         ('IN_PROGRESS', 'In Progress'),
         ('COMPLETED', 'Completed'),
    ]
    project = models.ForeignKey('Project', on_delete=models.CASCADE, default = 1)
    assigned_to = models.ManyToManyField(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #taskdetils_set = models.OneToOneField('TaskDetails', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

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
             on_delete=models.DO_NOTHING,
             related_name='details',
        )
        # assigned_to = models.CharField(max_length=100)
        priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
        notes = models.TextField(blank=True, null=True)

        def __str__(self):
            return f"Details for {self.task.title} - Priority: {self.get_priority_display()}"

class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def  __str__(self):
        return self.name
    
#signals
# @receiver(pre_save, sender=Task) #no created signal for pre_save
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_emp_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]

        send_mail(
            "New Task Assigned",
            f"A new task '{instance.title}' has been assigned to you.",
            "chanmia685@gmail.com",
            assigned_emails,
            fail_silently=False
        )

@receiver(post_delete, sender=Task)
def delete_task_details(sender, instance, **kwargs):
    if instance.details:
        instance.details.delete()
        print(f"Task details for '{instance.title}' deleted.")