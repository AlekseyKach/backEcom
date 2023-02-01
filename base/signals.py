from django.db.models.signals import pre_save
from django.contrib.auth.models import User


# make the email and username be the same 
def updateUSer(sender,instance,**kwargs):
    user = instance
    if user.email != "":
        user.username = user.email

pre_save.connect(updateUSer,sender=User)
