from django import forms
from .models import TypeSensUser

class TypeSensUserForm(forms.ModelForm):

    class Meta:
        model = TypeSensUser
        fields = [  'TypeCount', 'CountVals', 'DrawingType', 'Priority']
