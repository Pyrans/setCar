from django.db import models

# Create your models here.


class CarMessage(models.Model):
    # c_id = models.IntegerField(primary_key=True, auto_created=True, default=0)
    c_name = models.CharField(max_length=100, default='商务车')
    c_number = models.CharField(max_length=100, default=00000000)
    c_status = models.BooleanField(default=True)
    objects = models.Manager()


class PlanForCar(models.Model):
    # p_id = models.IntegerField(primary_key=True, auto_created=True, default=0)
    p_name = models.CharField(max_length=18)
    p_do = models.CharField(max_length=500)
    p_time_begin = models.DateTimeField()
    p_time_end = models.DateTimeField()
    p_time_create = models.DateTimeField(auto_now_add=True)
    p_time_change = models.DateTimeField(auto_now=True)
    p_status = models.BooleanField(default=True)
    p_car = models.CharField(max_length=200)
    objects = models.Manager()

