from django import forms
from .models import GroupUser

class GroupUserForm(forms.ModelForm):

    class Meta:
        model = GroupUser
        fields = [ 'Group', 'TypeCount', 'CountVals', 'DrawingType', 'Priority']
