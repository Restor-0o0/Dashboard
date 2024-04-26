from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver



class TypeSens(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    MetricUnits = models.CharField(max_length=100)
    Comment = models.CharField(max_length=250)

    def __str__(self):
        return self.Name

class Role(models.Model):
    ID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return self.Role


class Object(models.Model):
    ID = models.AutoField(primary_key=True)
    Address = models.CharField(max_length=250)

    def __str__(self):
        return self.Address


class TimeMark(models.Model):
    ID = models.AutoField(primary_key=True)
    DateTime = models.DateTimeField()

    def __str__(self):
        return self.DateTime.strftime("%Y-%m-%d %H:%M:%S")


class UserDate(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=250)

    def __str__(self):
        return self.Comment


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

    def __str__(self):
        return self.Name


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

    def __str__(self):
        return self.Name


class TypesCount(models.Model):
    ID = models.AutoField(primary_key=True)
    Nume = models.CharField(max_length=10)

    def __str__(self):
        return self.Nume
class Groups(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Comment = models.CharField(max_length=250)

    def __str__(self):
        return self.Name


class SensGroup(models.Model):
    Sensor = models.ForeignKey(Sensor,  on_delete=models.CASCADE)
    Group = models.ForeignKey(Groups,  on_delete=models.CASCADE)

class Meta:
        unique_together = ("Sensor", "Group")


class GroupUser(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    TypeCount = models.ForeignKey(TypesCount,on_delete=models.CASCADE)
    CountVals = models.IntegerField()
    DrawingType = models.ForeignKey(DrawingType, on_delete=models.SET_NULL, null=True)
    Priority = models.IntegerField(default=0)

    class Meta:
        unique_together = ("User", "Group","DrawingType")
