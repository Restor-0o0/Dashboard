from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver



class TypeSens(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    MetricUnits = models.CharField(max_length=100)
    Comment = models.CharField(max_length=250)

class Role(models.Model):
    ID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

class Object(models.Model):
    ID = models.AutoField(primary_key=True)
    Address = models.CharField(max_length=250)

class TimeMark(models.Model):
    ID = models.AutoField(primary_key=True)
    DateTime = models.DateTimeField(auto_now_add=True)


class UserDate(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=250)

    class Meta:
    # Указываем комбинацию полей, которая должна быть уникальной
        unique_together = ("Role", "User")

class TypeSensRole(models.Model):
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Type = models.ForeignKey(TypeSens, on_delete=models.CASCADE)

    class Meta:
        # Указываем комбинацию полей, которая должна быть уникальной
        unique_together = ("Role", "Type")


class Sensor(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Type = models.ForeignKey(TypeSens, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=250)


class SensObject(models.Model):
    ID = models.AutoField(primary_key=True)
    Object = models.ForeignKey(Object, on_delete=models.CASCADE)
    Sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)


class DataSens(models.Model):
    Sens = models.ForeignKey(Sensor,  on_delete=models.CASCADE)
    Time = models.ForeignKey(TimeMark, on_delete=models.CASCADE)
    Value = models.FloatField()


    class Meta:
        # Указываем комбинацию полей, которая должна быть уникальной
        unique_together = ("Sens", "Time")



class UserObject(models.Model):
    ID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Object = models.ForeignKey(Object, on_delete=models.CASCADE)
    Active = models.BooleanField(default=False)


class DrawingType(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Comment = models.CharField(max_length=250)


class TypeSensUser(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Type = models.ForeignKey(TypeSens, on_delete=models.CASCADE)
    DrawingType = models.ForeignKey(DrawingType, on_delete=models.SET_NULL, null=True)
    Priority = models.IntegerField()

    class Meta:
        unique_together = ("User", "Type")



@receiver(pre_save, sender=TypeSensUser)
def set_priority(sender, instance, *args, **kwargs):
    if not instance.Priority:
        instance.Priority = instance.Type.id
