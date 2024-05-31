from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .utils import graph1_func,graph2_func
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from statistics import mean
from .models import TypesCount,TypeSens,Role,Object,TimeMark,UserDate,TypeSensRole,Sensor,SensObject,DataSens,UserObject,DrawingType,GroupUser,Groups,SensGroup
from .forms import GroupUserForm
from django import forms
from django.db.models import Avg
from django.db.models.functions import TruncHour,TruncWeek,TruncDay,TruncMonth
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
from rest_framework.views import APIView
from .Serializer import SensorSerializer,GroupUserSerializer,DataSerializer,DataDrawingType,DataTypesCount
from rest_framework import permissions,viewsets
from rest_framework.response import Response
from rest_framework import serializers



class SettingsForms():
    Form = GroupUserForm()
    Name = ''

    def __init__(self,Form,Name):
        self.Form = Form
        self.Name = Name

def form_handler(request):
    if request.method == 'POST':
        instance = GroupUser.objects.get()
        form = GroupUser(request.POST,instance=instance)
        #print(request.POST.get('User'),request.POST.get('Group'),request.POST.get('DrawingType'))
        #print('method')
        if form.is_valid():
            form.save()
            #print('save_______________________________________')


@login_required
def index(request):

    if request.method == 'POST':
        instance = GroupUser.objects.get(pk=request.POST.get('ID'))
        form = GroupUserForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()

    num_graphs = 0
    head = []
    labels = []
    graph = []
    num_numbs = 0
    numbs = []
    metrics = []
    head_numb = []
    UserTypes = GroupUser.objects.filter(User=request.user).order_by('DrawingType','Priority')
    formsheaders = []

    formsheaders = {str(form.Group.ID): form.Group.Name for form in UserTypes}

    formss = []
    for UserType in UserTypes:
        elem = SettingsForms(GroupUserForm(instance=UserType),str(UserType.Group.Comment)+'('+str(UserType.DrawingType.Name)+')')
        elem.Form.fields['ID'].initial = UserType.pk
        formss.append(elem)

    ActiveObject = UserObject.objects.filter(User=request.user,Active=True).first().Object

    ActiveGroups = GroupUser.objects.filter(User=request.user).order_by('Priority')


    for obj in ActiveGroups:
        sens = SensGroup.objects.filter(Group=obj.Group).values_list('Sensor', flat=True)
        Types = Sensor.objects.filter(ID__in=sens.values_list('Sensor_id', flat=True)).values_list('Type', flat=True)
        Types = TypeSens.objects.filter(ID__in=Types)

        if('Number' in obj.DrawingType.Name):
            if(obj.TypeCount.Name == 'Day'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(days=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                if datavalues.exists():
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits    )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1


            elif(obj.TypeCount.Name == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                if datavalues.exists():
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1

            elif(obj.TypeCount.Name == 'Hour'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(hours=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                if datavalues.exists():
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits)
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1


            elif(obj.TypeCount.Name == 'Week'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(weeks=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                if datavalues.exists():
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1


            elif(obj.TypeCount.Name == 'Month'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(weeks=(4*obj.CountVals))

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                if datavalues.exists():
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1



        if('Graph' in obj.DrawingType.Name):
            if(obj.TypeCount.Name == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                timemark = DataSens.objects.filter(Sens__in=sens).values_list('Time', flat=True).order_by('id')[:int(obj.CountVals)]
                time_ = TimeMark.objects.filter(ID__in=timemark).values_list('DateTime', flat=True)
                head.append(obj.Group.Comment)
                labels.append([time.strftime(" %H:%M:%S") for time in time_])
                graph.append(list(datavalues))
                num_graphs = num_graphs+1

            elif(obj.TypeCount.Name == 'Hour'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(hours=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').order_by('hour').annotate(avg_val=Avg('Value'))

                if datavalues.exists():
                    head.append(obj.Group.Comment)
                    labels.append([time.strftime("%H") for time in list(datavalues.values_list('hour', flat=True))])
                    graph.append(list(datavalues.values_list('avg_val', flat=True)))
                    num_graphs = num_graphs+1


            elif(obj.TypeCount.Name == 'Day'):

                current_time = timezone.now()

                Days_ago = current_time - timedelta(days=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Days_ago ,Time__DateTime__lte=current_time).annotate(day_=TruncDay('Time__DateTime')).values('day_').order_by('day_').annotate(avg_val=Avg('Value'))

                if datavalues.exists():
                    head.append(obj.Group.Comment)
                    labels.append([time.strftime(" %d") for time in list(datavalues.values_list('day_', flat=True))])
                    graph.append(list(datavalues.values_list('avg_val', flat=True)))
                    num_graphs = num_graphs+1


            elif(obj.TypeCount.Name == 'Week'):

                current_time = timezone.now()

                Weeks_ago = current_time - timedelta(weeks=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Weeks_ago ,Time__DateTime__lte=current_time).annotate(Week=TruncWeek('Time__DateTime')).values('Week').order_by('Week').annotate(avg_val=Avg('Value'))

                if datavalues.exists():
                    head.append(obj.Group.Comment)
                    labels.append([time.strftime(" %d") for time in list(datavalues.values_list('Week', flat=True))])
                    graph.append(list(datavalues.values_list('avg_val', flat=True)))
                    num_graphs = num_graphs+1


            elif(obj.TypeCount.Name == 'Month') :

                current_time = timezone.now()

                Months_ago = current_time - timedelta(weeks=(4*obj.CountVals))

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Months_ago ,Time__DateTime__lte=current_time).annotate(Month=TruncMonth('Time__DateTime')).values('Month').order_by('Month').annotate(avg_val=Avg('Value'))

                if datavalues.exists():
                    head.append(obj.Group.Comment)
                    labels.append([time.strftime(" %m") for time in list(datavalues.values_list('Month', flat=True))])
                    graph.append(list(datavalues.values_list('avg_val', flat=True)))
                    num_graphs = num_graphs+1





    context = {
        'num_graphs': range(num_graphs),
        'graph': graph,
        'labels': labels,
        'head': head,
        'num_numbs': range(num_numbs),
        'numbs': numbs,
        'metrics': metrics,
        'head_numb': head_numb,
        'forms': formss,
        'formsheaders': formsheaders,
    }
    return render(request, 'main/index.html',  context)

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/log.html'

    def get_success_url(self):
        return reverse_lazy('index')



class DataAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        num_graphs = 0
        head = []
        labels = []
        graph = []
        num_numbs = 0
        numbs = []
        metrics = []
        head_numb = []
        UserTypes = GroupUser.objects.filter(User=request.user).order_by('DrawingType','Priority')
        formsheaders = []

        formsheaders = {str(form.Group.ID): form.Group.Name for form in UserTypes}

        formss = []
        for UserType in UserTypes:
            elem = SettingsForms(GroupUserForm(instance=UserType),str(UserType.Group.Comment)+'('+str(UserType.DrawingType.Name)+')')
            elem.Form.fields['ID'].initial = UserType.pk
            formss.append(elem)

        ActiveObject = UserObject.objects.filter(User=request.user,Active=True).first().Object

        ActiveGroups = GroupUser.objects.filter(User=request.user).order_by('Priority')


        for obj in ActiveGroups:
            sens = SensGroup.objects.filter(Group=obj.Group).values_list('Sensor', flat=True)
            Types = Sensor.objects.filter(ID__in=sens.values_list('Sensor_id', flat=True)).values_list('Type', flat=True)
            Types = TypeSens.objects.filter(ID__in=Types)

            if('Number' in obj.DrawingType.Name):
                if(obj.TypeCount.Name == 'Day'):

                    current_time = timezone.now()

                    hours_ago = current_time - timedelta(days=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                    if datavalues.exists():
                        numbs.append(round(mean(datavalues),1))
                        metrics.append(Types.first().MetricUnits    )
                        head_numb.append(obj.Group.Comment)
                        num_numbs = num_numbs+1



                elif(obj.TypeCount.Name == 'Record'):
                    Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                    datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                    if datavalues.exists():
                        numbs.append(round(mean(datavalues),1))
                        metrics.append(Types.first().MetricUnits   )
                        head_numb.append(obj.Group.Comment)
                        num_numbs = num_numbs+1

                elif(obj.TypeCount.Name == 'Hour'):

                    current_time = timezone.now()

                    hours_ago = current_time - timedelta(hours=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                    if datavalues.exists():
                        numbs.append(round(mean(datavalues),1))
                        metrics.append(Types.first().MetricUnits)
                        head_numb.append(obj.Group.Comment)
                        num_numbs = num_numbs+1


                elif(obj.TypeCount.Name == 'Week'):

                    current_time = timezone.now()

                    hours_ago = current_time - timedelta(weeks=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                    if datavalues.exists():
                        numbs.append(round(mean(datavalues),1))
                        metrics.append(Types.first().MetricUnits   )
                        head_numb.append(obj.Group.Comment)
                        num_numbs = num_numbs+1


                elif(obj.TypeCount.Name == 'Month'):

                    current_time = timezone.now()

                    hours_ago = current_time - timedelta(weeks=(4*obj.CountVals))

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)

                    if datavalues.exists():
                        numbs.append(round(mean(datavalues),1))
                        metrics.append(Types.first().MetricUnits   )
                        head_numb.append(obj.Group.Comment)
                        num_numbs = num_numbs+1


            if('Graph' in obj.DrawingType.Name):
                if(obj.TypeCount.Name == 'Record'):
                    Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                    datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                    timemark = DataSens.objects.filter(Sens__in=sens).values_list('Time', flat=True).order_by('id')[:int(obj.CountVals)]
                    time_ = TimeMark.objects.filter(ID__in=timemark).values_list('DateTime', flat=True)
                    head.append(obj.Group.Comment)
                    labels.append([time.strftime(" %H:%M:%S") for time in time_])
                    graph.append(list(datavalues))
                    num_graphs = num_graphs+1

                elif(obj.TypeCount.Name == 'Hour'):

                    current_time = timezone.now()

                    hours_ago = current_time - timedelta(hours=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').order_by('hour').annotate(avg_val=Avg('Value'))

                    if datavalues.exists():
                        head.append(obj.Group.Comment)
                        labels.append([time.strftime("%H") for time in list(datavalues.values_list('hour', flat=True))])
                        graph.append(list(datavalues.values_list('avg_val', flat=True)))
                        num_graphs = num_graphs+1


                elif(obj.TypeCount.Name == 'Day'):

                    current_time = timezone.now()

                    Days_ago = current_time - timedelta(days=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Days_ago ,Time__DateTime__lte=current_time).annotate(day_=TruncDay('Time__DateTime')).values('day_').order_by('day_').annotate(avg_val=Avg('Value'))

                    if datavalues.exists():
                        head.append(obj.Group.Comment)
                        labels.append([time.strftime(" %d") for time in list(datavalues.values_list('day_', flat=True))])
                        graph.append(list(datavalues.values_list('avg_val', flat=True)))
                        num_graphs = num_graphs+1


                elif(obj.TypeCount.Name == 'Week'):

                    current_time = timezone.now()

                    Weeks_ago = current_time - timedelta(weeks=obj.CountVals)

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Weeks_ago ,Time__DateTime__lte=current_time).annotate(Week=TruncWeek('Time__DateTime')).values('Week').order_by('Week').annotate(avg_val=Avg('Value'))

                    if datavalues.exists():
                        head.append(obj.Group.Comment)
                        labels.append([time.strftime(" %d") for time in list(datavalues.values_list('Week', flat=True))])
                        graph.append(list(datavalues.values_list('avg_val', flat=True)))
                        num_graphs = num_graphs+1


                elif(obj.TypeCount.Name == 'Month') :

                    current_time = timezone.now()

                    Months_ago = current_time - timedelta(weeks=(4*obj.CountVals))

                    datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=Months_ago ,Time__DateTime__lte=current_time).annotate(Month=TruncMonth('Time__DateTime')).values('Month').order_by('Month').annotate(avg_val=Avg('Value'))

                    if datavalues.exists():
                        head.append(obj.Group.Comment)
                        labels.append([time.strftime(" %m") for time in list(datavalues.values_list('Month', flat=True))])
                        graph.append(list(datavalues.values_list('avg_val', flat=True)))
                        num_graphs = num_graphs+1

        context = {
            'login': request.user.username,
            'num_graphs': num_graphs,
            'graph': graph,
            'labels': labels,
            'head': head,
            'num_numbs': num_numbs,
            'numbs': numbs,
            'metrics': metrics,
            'head_numb': head_numb,
            'forms': formss,
            'formsheaders': formsheaders,

        }

        serializerdata = DataSerializer(data=context)
        serializerdata.is_valid(raise_exception=True)
        return Response(serializerdata.data)

class DataSettingsViewAPIView(generics.UpdateAPIView):
    queryset = GroupUser.objects.all()
    serializer_class = GroupUserSerializer




class SettingsAPIView(viewsets.ModelViewSet):
    serializer_class = GroupUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return GroupUser.objects.filter(User=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DrawingTypeViewSet(generics.ListAPIView):
    queryset = DrawingType.objects.all()
    serializer_class = DataDrawingType


class TypesCountViewSet(generics.ListAPIView):
    queryset = TypesCount.objects.all()
    serializer_class = DataTypesCount
