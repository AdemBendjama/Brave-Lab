from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group


phone_regex = RegexValidator(
    regex=r'^0[5-7][0-9]{8}$',
    message='Please enter a valid phone number starting with 05, 06 or 07 and has 10 digits in total'
)

class Client(models.Model):
    GENDERS =[
        ('M','Male'),
        ('F','Female')
    ]
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,validators=[phone_regex])
    gender = models.CharField(max_length = 1 ,choices = GENDERS)
    address = models.CharField(max_length=50)
    policy = models.BooleanField(default = False)
    
    
    class Meta():
        db_table = 'auth_client'
        
    def __str__(self):
        return f'{self.user.username}'
    