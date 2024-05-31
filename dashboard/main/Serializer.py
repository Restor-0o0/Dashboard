from rest_framework import serializers
from .models import Sensor,GroupUser,DrawingType,TypesCount,Groups




class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'



class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class GroupUserSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(source='Group.Name')
    class Meta:
        model = GroupUser
        fields = ('ID','User','Group','TypeCount','DrawingType','Priority','CountVals','Name',)
        read_only = ['ID','User','Group']


class DataTypesCount(serializers.ModelSerializer):
    class Meta:
        model = TypesCount
        fields = '__all__'

class DataDrawingType(serializers.ModelSerializer):
    class Meta:
        model = DrawingType
        fields = '__all__'

class DataSerializer(serializers.Serializer):
    login = serializers.CharField()
    num_graphs = serializers.IntegerField()
    graph = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
    labels = serializers.ListField(child=serializers.ListField(child=serializers.CharField()))
    head = serializers.ListField(child=serializers.CharField())
    num_numbs = serializers.IntegerField()
    numbs = serializers.ListField(child=serializers.FloatField())
    metrics = serializers.ListField(child=serializers.CharField())
    head_numb = serializers.ListField(child=serializers.CharField())
