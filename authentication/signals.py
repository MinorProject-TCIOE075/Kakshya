from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Student, Teacher


User = get_user_model()

"""
  Signals in django is a function or feature that is based on Observer Design Pattern.
  Signals is a trigger method that does a specific task when some kind of function or
  command is triggered. for example: when a user is registered his/her profile is automatically
  created.
  For signal to work there must be 2 key elements i.e. Sender and receiver
  Sender is either a Python object or None which dispatches a signal to the receiver.
  The receiver is a function or an instance which receives the signal dispatched by the
  sender. Most of the time a receiver is an instance of a model like a user instance.  
"""

""" 
    The following are two signals methods, the 1st one creates a Student user isntance or
    a teacher user instance based on the conditions it satisfy.
    There are two methods in django signals to dispatch and receive signals:
    We used the receiver decorator method which take two arguments, the 1st one is post_save 
    and second argument is the sender which may be an object or a model instance.

    using post_save below in the 1st method means the signal will be dispatched after the User instance is 
    created, in our case create a Student or a Teacher instance after a user is created.

    in the 2nd method the model instance is saved to the database after it checks the user_role.

"""
@receiver(post_save, sender=User)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        print(created)
        if instance.user_role == 'S':
            Student.objects.create(user=instance)
        elif instance.user_role == 'T':
            Teacher.objects.create(user=instance)
        
        else:
            pass


@receiver(post_save, sender=User)
def save_user_student(sender, instance, **kwargs):
    if instance.user_role == 'S':
        instance.student.save()

    
    # the teacher attribute below comes from related_name attribute from the OneToOneField in
    # the Teacher model. same is the case for the "student" attribute above.

    elif instance.user_role == 'T':
        instance.teacher.save()

    else: 
        pass
