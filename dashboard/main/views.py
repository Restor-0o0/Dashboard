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
from django.db.models.functions import TruncHour
from django.utils import timezone
from datetime import timedelta

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
        print(request.POST.get('User'),request.POST.get('Group'),request.POST.get('DrawingType'))
        print('method')
        if form.is_valid():
            form.save()
            print('save_______________________________________')


@login_required
def index(request):

    if request.method == 'POST':
        print(request.POST.keys())
        instance = GroupUser.objects.get(pk=request.POST.get('ID'))
        form = GroupUserForm(request.POST,instance=instance)
        print(request.user,request.POST.get('Group'),request.POST.get('DrawingType'))
        print('method')
        if form.is_valid():
            form.save()
            print('save_______________________________________')

    num_graphs = 0
    head = []
    labels = []
    graph = []
    num_numbs = 0
    numbs = []
    metrics = []
    head_numb = []
    UserTypes = GroupUser.objects.filter(User=request.user).order_by('DrawingType','Priority')
    print(UserTypes)
    formsheaders = []

    print(UserTypes.values('ID'))
    formsheaders = {str(form.Group.ID): form.Group.Name for form in UserTypes}

    formss = []
    for UserType in UserTypes:
        elem = SettingsForms(GroupUserForm(instance=UserType),str(UserType.Group.Comment)+'('+str(UserType.DrawingType.Name)+')')
        elem.Form.fields['ID'].initial = UserType.pk
        formss.append(elem)

    print(formss[0].Form.fields)
    ActiveObject = UserObject.objects.filter(User=request.user,Active=True).first().Object

    ActiveGroups = GroupUser.objects.filter(User=request.user).order_by('Priority')


    for obj in ActiveGroups:
        sens = SensGroup.objects.filter(Group=obj.Group).values_list('Sensor', flat=True)
        Types = Sensor.objects.filter(ID__in=sens.values_list('Sensor_id', flat=True)).values_list('Type', flat=True)
        Types = TypeSens.objects.filter(ID__in=Types)
        print(Types)
        print('____________________________-')
        #sens = Sensor.objects.filter(ID__in=SensObject.objects.filter(Object=ActiveObject,Sensor__in=Sensor.objects.filter(Type__in=Types)))

        if('Number' in obj.DrawingType.Name):
            if(obj.TypeCount.Nume == 'Day'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(days=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)
                #datavalues = datavalues.values_list('avg_val', flat=True)
                print(datavalues)
              #  for vl in datavalues:
               #     print( vl['hour'],'___',vl['avg_val'])

                try:
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits    )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1
                except:
                    pass

                print(numbs)
                print(metrics)
                print(head_numb)
            elif(obj.TypeCount.Nume == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]

                numbs.append(round(mean(datavalues),1))
                metrics.append(Types.first().MetricUnits   )
                head_numb.append(obj.Group.Comment)
                num_numbs = num_numbs+1
                print(numbs)
                print(metrics)
                print(head_numb)
            elif(obj.TypeCount.Nume == 'Hour'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(hours=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)
                #datavalues = datavalues.values_list('avg_val', flat=True)
                print(datavalues)
              #  for vl in datavalues:
               #     print( vl['hour'],'___',vl['avg_val'])
                try:
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1

                except:
                    pass
                print(numbs)
                print(metrics)
                print(head_numb)
            elif(obj.TypeCount.Nume == 'Week'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(weeks=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)
                #datavalues = datavalues.values_list('avg_val', flat=True)
                print(datavalues)
              #  for vl in datavalues:
               #     print( vl['hour'],'___',vl['avg_val'])

                try:
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1
                except:
                    pass

                print(numbs)
                print(metrics)
                print(head_numb)
            elif(obj.TypeCount.Nume == 'Month'):

                current_time = timezone.now()

                hours_ago = current_time - timedelta(months=obj.CountVals)

                datavalues = DataSens.objects.select_related('Time').filter(Sens__in=sens,Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value')).values_list('avg_val', flat=True)
                #datavalues = datavalues.values_list('avg_val', flat=True)
                print(datavalues)
              #  for vl in datavalues:
               #     print( vl['hour'],'___',vl['avg_val'])

                try:
                    numbs.append(round(mean(datavalues),1))
                    metrics.append(Types.first().MetricUnits   )
                    head_numb.append(obj.Group.Comment)
                    num_numbs = num_numbs+1
                except:
                    pass

                print(numbs)
                print(metrics)
                print(head_numb)

        if('Graph' in obj.DrawingType.Name):
            if(obj.TypeCount.Nume == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                timemark = DataSens.objects.filter(Sens__in=sens).values_list('Time', flat=True).order_by('id')[:int(obj.CountVals)]
                time_ = TimeMark.objects.filter(ID__in=timemark).values_list('DateTime', flat=True)
                head.append(obj.Group.Comment)
                labels.append([time.strftime(" %H:%M:%S") for time in time_])
                graph.append(list(datavalues))
                num_graphs = num_graphs+1
                print(graph)
                print(labels)
                print(head)

                #current_time = timezone.now()

                # Вычитаем 5 часов из текущего времени
                #hours_ago = current_time - timedelta(hours=obj.CountVals)

                #datavalues = DataSens.objects.select_related('Time').filter(Time__DateTime__gte=hours_ago ,Time__DateTime__lte=current_time).annotate(hour=TruncHour('Time__DateTime')).values('hour').annotate(avg_val=Avg('Value'))[:]





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
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


# Create your views here.,  {'graph1': graph1, 'graph2': graph2}
