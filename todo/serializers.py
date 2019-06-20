from .models import Task,List
from rest_framework import serializers



#Serializer to create display datata of lists
class ListSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField( #Set to create url links
        many=True,
        read_only=True,
        view_name='task-detail',
        lookup_field='slug',
        ) #Rules to collect data

    class Meta:
        model = List #Dataset to collect data
        fields = ('url', 'title','tasks', 'key') #Show fields
        lookup_field = 'slug',
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}}


#Inheriance from ListSerializer
class ListSerializerFilterNotComplete(ListSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail',
        lookup_field='slug',
        source='filtered_non_complete' # Ensure resulted dataset will contain only non complete
    )
#Inheriance from ListSerializer
class ListSerializerFilterComplete(ListSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail',
        lookup_field='slug',
        source='filtered_complete' # Ensure resulted dataset will contain only complete
    )


class ListSerializer_Slug(ListSerializer):
    tasks = serializers.HyperlinkedRelatedField( #Set to create url links
        many=True,
        read_only=True,
        view_name='task-detail',
        lookup_field='slug',
        ) #Rules to collect data

    class Meta:
        model = List #Dataset to collect data
        fields = ('url', 'title','tasks','slug') #Show fields
        lookup_field = 'slug',
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}}


#Serializer to create display datata of lists
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    list = serializers.HyperlinkedRelatedField(
        queryset=List.objects.all(),
        lookup_field='slug',
        view_name='list-detail'
    )

    class Meta:
        model = Task
        fields = ('url','name','complete','list','slug','created_at','updated_at')
        lookup_field = 'slug',
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }