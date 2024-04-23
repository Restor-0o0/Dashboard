from django.contrib import admin
from .models import TypesCount,TypeSens,Role,Object,TimeMark,UserDate,TypeSensRole,Sensor,SensObject,DataSens,UserObject,DrawingType,TypeSensUser



class TypeSensAdmin(admin.ModelAdmin):
    list_display = ('ID','Name','MetricUnits','Comment')
    def __str__(self):
        return self.Name


class RoleAdmin(admin.ModelAdmin):
    list_display = ('ID','Role','comment')

    def __str__(self):
        return self.comment

class ObjectAdmin(admin.ModelAdmin):
    list_display = ('ID','Address')

    def __str__(self):
        return self.Address


class TimeMarkAdmin(admin.ModelAdmin):
    list_display = ('ID','DateTime')

    def __str__(self):
        return self.DateTime

class UserDateAdmin(admin.ModelAdmin):
    list_display = ('User','Role','Comment')

    def __str__(self):
        return self.Comment

class TypeSensRoleAdmin(admin.ModelAdmin):
    list_display = ('Role','Type')

class SensorAdmin(admin.ModelAdmin):
    list_display = ('ID','Name','Type','Comment')
    def __str__(self):
        return self.Name

class SensObjectAdmin(admin.ModelAdmin):
    list_display = ('ID','Object','Sensor')

class DataSensAdmin(admin.ModelAdmin):
    list_display = ('Sens','Time','Value')

class UserObjectAdmin(admin.ModelAdmin):
    list_display = ('ID','User','Object','Active')


class DrawingTypeAdmin(admin.ModelAdmin):
    list_display = ('ID','Name','Comment')
    def __str__(self):
        return self.Name

class TypeSensUserAdmin(admin.ModelAdmin):
    list_display = ('User','Type','DrawingType','Priority')

class TypesCountAdmin(admin.ModelAdmin):
    list_display = ('ID','Nume')
    def __str__(self):
        return self.Nume


admin.site.register(TypesCount,TypesCountAdmin)
admin.site.register(TypeSens,TypeSensAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(Object,ObjectAdmin)
admin.site.register(TimeMark,TimeMarkAdmin)
admin.site.register(UserDate,UserDateAdmin)
admin.site.register(TypeSensRole,TypeSensRoleAdmin)
admin.site.register(Sensor,SensorAdmin)
admin.site.register(SensObject,SensObjectAdmin)
admin.site.register(DataSens,DataSensAdmin)
admin.site.register(UserObject,UserObjectAdmin)
admin.site.register(DrawingType,DrawingTypeAdmin)
admin.site.register(TypeSensUser,TypeSensUserAdmin)
# Register your models here.
