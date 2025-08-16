from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from task.models import Task

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