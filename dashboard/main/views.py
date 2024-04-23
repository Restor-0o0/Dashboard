from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .utils import graph1_func,graph2_func
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from statistics import mean
from .models import TypesCount,TypeSens,Role,Object,TimeMark,UserDate,TypeSensRole,Sensor,SensObject,DataSens,UserObject,DrawingType,TypeSensUser
from .forms import TypeSensUserForm
from django import forms

class SettingsForms():
    Form = TypeSensUserForm()
    Name = ''

    def __init__(self,Form,Name):
        self.Form = Form
        self.Name = Name

def form_handler(request):
    if request.method == 'POST':
        instance = TypeSensUser.objects.get(User=request.POST.get('User'),Type=request.POST.get('Type'),DrawingType=request.POST.get('DrawingType'))
        form = TypeSensUserForm(request.POST,instance=instance)
        print(request.POST.get('User'),request.POST.get('Type'),request.POST.get('DrawingType'))
        print('method')
        if form.is_valid():
            form.save()
            print('save_______________________________________')


@login_required
def index(request):

    if request.method == 'POST':
        instance = TypeSensUser.objects.get(User=request.POST.get('User'),Type=request.POST.get('Type'),DrawingType=request.POST.get('DrawingType'))
        form = TypeSensUserForm(request.POST,instance=instance)
        print(request.POST.get('User'),request.POST.get('Type'),request.POST.get('DrawingType'))
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
    UserTypes = TypeSensUser.objects.filter(User=request.user).order_by('DrawingType','Priority')
    print(UserTypes)
    formsheaders = []


    #forms = { str(UserType.Type.Name): TypeSensUserForm(instance=UserType) for UserType in UserTypes}
    formsheaders = {str(form.Type.ID): form.Type.Name for form in UserTypes}

    formss = [SettingsForms(TypeSensUserForm(instance=UserType),str(UserType.Type.Comment)+'('+str(UserType.DrawingType.Name)+')') for UserType in UserTypes]
        #form.Form.fields['Priority'].widget = forms.Select(choices=list(TypeSensUser.objects.filter(User=request.user,DrawingType=DrawingType.objects.get(Name=form.Form.fields['DrawingType']))).values('Priority'))
    ActiveObject = UserObject.objects.filter(User=request.user,Active=True).first().Object

    ActiveTypes = TypeSensUser.objects.filter(User=request.user).order_by('Priority')


    for obj in ActiveTypes:
        # = SensObject.objects.filter(Object=ActiveObject)
        #senss = sens.filter(Sensor__in=Sensor.objects.filter(Type=obj.Type))

        sens = Sensor.objects.filter(ID__in=SensObject.objects.filter(Object=ActiveObject,Sensor__in=Sensor.objects.filter(Type=obj.Type)))

        if(obj.DrawingType.Name == 'Number'):
            if(obj.TypeCount.Nume == 'Day'):
                pass
            elif(obj.TypeCount.Nume == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                numbs.append(round(mean(datavalues),1))
                metrics.append(obj.Type.MetricUnits)
                head_numb.append(obj.Type.Comment)
                num_numbs = num_numbs+1
                print(numbs)
                print(metrics)
                print(head_numb)
            elif(obj.TypeCount.Nume == 'Hour'):
                pass
            elif(obj.TypeCount.Nume == 'Week'):
                pass
            elif(obj.TypeCount.Nume == 'Month'):
                pass

        elif(obj.DrawingType.Name == 'Graph'):
            if(obj.TypeCount.Nume == 'Record'):
                Sensors = SensObject.objects.filter(Object=ActiveObject).values('Sensor')
                datavalues = DataSens.objects.filter(Sens__in=sens).values_list('Value', flat=True).order_by('id')[:int(obj.CountVals)]
                timemark = DataSens.objects.filter(Sens__in=sens).values_list('Time', flat=True).order_by('id')[:int(obj.CountVals)]
                time_ = TimeMark.objects.filter(ID__in=timemark).values_list('DateTime', flat=True)
                head.append(obj.Type.Comment)
                labels.append([time.strftime(" %H:%M:%S") for time in time_])
                graph.append(list(datavalues))
                num_graphs = num_graphs+1
                print(graph)
                print(labels)
                print(head)






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
