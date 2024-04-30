from django import forms
from .models import GroupUser

class GroupUserForm(forms.ModelForm):
    ID = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = GroupUser
        fields = ['ID','Group', 'TypeCount', 'CountVals', 'DrawingType', 'Priority']
